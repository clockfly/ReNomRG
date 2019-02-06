import enum
import weakref
import os
import time
import numpy as np
from sklearn.metrics import r2_score
from sklearn import preprocessing
import pickle
import threading

import renom as rm
from renom.optimizer import Adam
from renom.cuda import release_mem_pool, use_device
from renom.utility.distributor.distributor import NdarrayDistributor

from renom_rg.server import (C_GCNN, Kernel_GCNN, DBSCAN_GCNN, USER_DEFINED,
                             DB_DIR_TRAINED_WEIGHT, DATASRC_DIR, SCRIPT_DIR)
from renom_rg.server.custom_util import _load_usermodel

from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.feature_graph import get_corr_graph, get_kernel_graph, get_dbscan_graph
from . import db


class RunningState(enum.Enum):
    TRAINING = 0
    FINISHED = 1


class TaskState:

    tasks = weakref.WeakValueDictionary()  # Mapping of {model.id: TaskState()}

    @classmethod
    def add_task(cls, model):
        ret = TaskState(model.id)
        cls.tasks[model.id] = ret
        return ret

    def __init__(self, model_id):
        self.error_msgs = []

        self.model_id = model_id
        self.state = RunningState.TRAINING
        self.canceled = False
        self.nth_epoch = -1
        self.nth_batch = -1
        self.train_loss = -1
        self.total_epoch = -1
        self.total_batch = -1
        self.algorithm = -1

    _lock = threading.RLock()
    _events = weakref.WeakSet()
    serial = 0

    @classmethod
    def add_event(cls, serial, event=None):
        if event is None:
            event = threading.Event()

        if serial is None:
            event.set()
            return event

        if serial is not None:
            if serial != cls.serial:
                # models already updated
                event.set()
                return event

        with cls._lock:
            cls._events.add(event)

        return event

    @classmethod
    def signal(cls):
        with cls._lock:
            cls.serial += 1
            if not cls._events:
                return
            ev = cls._events.pop()

        ev.set()


def split_target(data, ids):
    indexes = np.ones(data.shape[1], dtype=bool)
    indexes[ids] = False
    X = data[:, indexes]
    y = data[:, ids]
    return X, y


def calc_confidence_area(true_data, pred_data):
    num_bin = 10
    confidence_area = []
    for j, d in enumerate(true_data):
        hist, bins = np.histogram(d, bins=num_bin)

        confidence_data = None
        m = []
        l_i = 0
        for i in range(num_bin):
            true_data_index = np.logical_and(bins[i] < d, d < bins[i + 1])
            pred_data_in_bin = pred_data[j][true_data_index]

            if len(pred_data_in_bin) > 0:
                m.append(np.mean(pred_data_in_bin))
                sd = np.sqrt(np.sum((pred_data_in_bin - m[i])**2) / len(pred_data_in_bin))
                if sd == 0:
                    sd = 0.0000001
                c = np.array([m[i] - sd * 2, m[i] - sd, m[i], m[i] + sd, m[i] + sd * 2]).reshape(1, -1)
                l_i = i
            else:
                if l_i == 0:
                    m.append(0)
                else:
                    m.append(m[l_i])
                    c = np.array([m[i], m[i], m[i], m[i], m[i]]).reshape(1, -1)

            if confidence_data is None:
                # append histogram x_min data
                confidence_data = np.concatenate([c, c], axis=0)
            else:
                confidence_data = np.concatenate([confidence_data, c], axis=0)

        # append histogram x_max data
        confidence_data = np.concatenate([confidence_data, c], axis=0)
        confidence_area.append(confidence_data)
    return np.array(confidence_area)


def train(taskstate, model_id):
    session = db.session()
    try:
        taskstate.signal()
        return _train(session, taskstate, model_id)
    finally:
        taskstate.signal()
        session.commit()


def zscore(np_x):
    ss = preprocessing.StandardScaler()
    result = ss.fit_transform(np_x)
    return result

def min_max(np_x):
    mm = preprocessing.MinMaxScaler()
    result = mm.fit_transform(np_x)
    return result


def _train(session, taskstate, model_id):
    modeldef = session.query(db.Model).get(model_id)

    total_batch = 0
    best_loss = None
    train_loss_list = []
    valid_loss_list = []

    with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
        data = pickle.load(f)

    X, y = split_target(np.array(data), pickle.loads(modeldef.dataset.target_column_ids))

    selected_scaling = modeldef.dataset.selected_scaling
    if selected_scaling == 2:
        y = zscore(y)
        X = zscore(X)
    elif selected_scaling == 3:
        y = min_max(y)
        X = min_max(X)

    X_train = X[pickle.loads(modeldef.dataset.train_index)]
    X_valid = X[pickle.loads(modeldef.dataset.valid_index)]
    y_train = y[pickle.loads(modeldef.dataset.train_index)]
    y_valid = y[pickle.loads(modeldef.dataset.valid_index)]
    valid_true = y_valid

    taskstate.algorithm = modeldef.algorithm
    algorithm_params = pickle.loads(modeldef.algorithm_params)
    algorithm_params["num_target"] = y_train.shape[1]

    if modeldef.algorithm == USER_DEFINED:
        num_neighbors = int(algorithm_params["num_neighbors"])
        feature_graph = get_corr_graph(X_train, num_neighbors)
        algorithm_params["feature_graph"] = feature_graph.tolist()
        model = _load_usermodel(algorithm_params)
    else:
        num_neighbors = int(algorithm_params["num_neighbors"])
        if modeldef.algorithm == C_GCNN:
            feature_graph = get_corr_graph(X_train, num_neighbors)
        elif modeldef.algorithm == Kernel_GCNN:
            feature_graph = get_kernel_graph(X_train, num_neighbors, 0.01)
        elif modeldef.algorithm == DBSCAN_GCNN:
            feature_graph = get_dbscan_graph(X_train, num_neighbors)
        else:
            raise ValueError("{} is not supported algorithm id.".format(modeldef.algorithm))

        model = GCNet(feature_graph, num_target=y_train.shape[1],
                      fc_unit=[int(u) for u in algorithm_params["fc_unit"]],
                      neighbors=num_neighbors,
                      channels=[int(u) for u in algorithm_params["channels"]])

        # update network params for prediciton
        algorithm_params["feature_graph"] = feature_graph.tolist()

    modeldef.algorithm_params = pickle.dumps(algorithm_params)

    filename = '{}.h5'.format(int(time.time()))
    optimizer = Adam()

    taskstate.total_epoch = modeldef.epoch
    for e in range(modeldef.epoch):
        taskstate.nth_epoch = e
        N = X_train.shape[0]
        perm = np.random.permutation(N)
        loss = 0
        train_true_list = None
        train_predicted_list = None

        total_batch = N // modeldef.batch_size
        taskstate.total_batch = total_batch
        for j in range(total_batch):
            if taskstate.canceled:
                return

            taskstate.nth_batch = j
            taskstate.signal()

            index = perm[j * modeldef.batch_size:(j + 1) * modeldef.batch_size]
            train_batch_x = X_train[index].reshape(-1, 1, X_train.shape[1], 1)
            train_batch_y = y_train[index]

            # Loss function
            model.set_models(inference=False)
            with model.train():
                train_predicted = model(train_batch_x)
                batch_loss = rm.mse(train_predicted, train_batch_y)
                taskstate.train_loss = batch_loss.tolist()

                if rm.is_cuda_active():
                    train_predicted = train_predicted.as_ndarray()

                if train_predicted_list is None:
                    train_predicted_list = train_predicted
                else:
                    train_predicted_list = np.concatenate([train_predicted_list, train_predicted])

                if train_true_list is None:
                    train_true_list = train_batch_y
                else:
                    train_true_list = np.concatenate([train_true_list, train_batch_y])

            # Back propagation
            grad = batch_loss.grad()

            # Update
            grad.update(optimizer)
            loss += batch_loss.as_ndarray()

            taskstate.signal()

        train_loss = loss / total_batch
        train_loss_list.append(float(train_loss))

        # validation
        model.set_models(inference=True)
        N = X_valid.shape[0]
        perm = np.random.permutation(N)
        total_batch = N // modeldef.batch_size
        loss = 0
        valid_predicted = None
        valid_true = None
        for j in range(total_batch):
            if taskstate.canceled:
                return

            index = perm[j * modeldef.batch_size:(j + 1) * modeldef.batch_size]
            batch_x = X_valid[index]
            batch_y = y_valid[index]

            predicted = model(batch_x.reshape(-1, 1, batch_x.shape[1], 1))
            loss += rm.mse(predicted, batch_y)

            if rm.is_cuda_active():
                predicted = predicted.as_ndarray()

            if valid_predicted is None:
                valid_predicted = predicted
                valid_true = batch_y
            else:
                valid_predicted = np.concatenate([valid_predicted, predicted], axis=0)
                valid_true = np.concatenate([valid_true, batch_y], axis=0)

        valid_loss = loss / total_batch
        valid_loss_list.append(float(valid_loss))

        # update model info
        modeldef.train_loss_list = pickle.dumps(train_loss_list)
        modeldef.valid_loss_list = pickle.dumps(valid_loss_list)

        SAMPLING_SIZE = 100

        sampled_valid_pred = valid_predicted[:SAMPLING_SIZE]
        sampled_valid_true = valid_true[:SAMPLING_SIZE]
        modeldef.valid_predicted = pickle.dumps(sampled_valid_pred.T.tolist())
        modeldef.valid_true = pickle.dumps(sampled_valid_true.T.tolist())

        sampled_train_pred = train_predicted_list[:SAMPLING_SIZE]
        sampled_train_true = train_true_list[:SAMPLING_SIZE]
        modeldef.sampled_train_pred = pickle.dumps(sampled_train_pred.T.tolist())
        modeldef.sampled_train_true = pickle.dumps(sampled_train_true.T.tolist())

        # true histogram
        true_histogram = []
        pred_histogram = []
        for i in range(y_valid.shape[1]):
            counts, bins = np.histogram(train_true_list[:, i])
            train_true_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
            counts, bins = np.histogram(y_valid[:, i])
            valid_true_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
            true_histogram.append({"train": train_true_histogram, "valid": valid_true_histogram})

            # pred histogram
            counts, bins = np.histogram(train_predicted_list[:, i])
            train_pred_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
            counts, bins = np.histogram(valid_predicted[:, i])
            valid_pred_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
            pred_histogram.append({"train": train_pred_histogram, "valid": valid_pred_histogram})

        modeldef.true_histogram = pickle.dumps(true_histogram)
        modeldef.pred_histogram = pickle.dumps(pred_histogram)

        # calc train data confidence area
        confidence_data_list = calc_confidence_area(train_true_list.T, train_predicted_list.T)
        modeldef.confidence_data = pickle.dumps(confidence_data_list.tolist())

        session.add(modeldef)
        session.commit()

        if e % 10 == 0:
            print("epoch: {}, valid_loss: {}".format(e, valid_loss))

        # update best loss model info
        if best_loss is None or best_loss > valid_loss:
            model.save(os.path.join(DB_DIR_TRAINED_WEIGHT, filename))

            modeldef.best_epoch = e
            modeldef.best_epoch_valid_loss = float(valid_loss)
            modeldef.best_epoch_rmse = float(np.sqrt(valid_loss))
            modeldef.best_epoch_max_abs_error = float(np.max(np.abs(valid_true - valid_predicted)))
            modeldef.best_epoch_r2 = float(r2_score(valid_true, valid_predicted))
            modeldef.weight = filename

            session.add(modeldef)
            session.commit()

            best_loss = valid_loss

    # TODO:
    # calc importances
    # NUM_PERM = 100
    # importances = []
    # for i in range(X_valid.shape[1]):
    #     tl = 0
    #     for k in range(NUM_PERM):
    #         p = np.random.permutation(X_valid.shape[0])
    #         X_randomized = np.copy(X_valid.T)
    #         X_randomized[i] = X_randomized[i, p]
    #         X_randomized = X_randomized.T
    #         pred = model(X_randomized.reshape(-1, 1, X_randomized.shape[1], 1))
    #         tl += float(rm.mse(pred, y_valid))
    #     importances.append(tl / NUM_PERM - valid_loss)
    #
    # print(importances)
    # print(np.array(importances) / np.sum(np.array(importances)))

    taskstate.state = RunningState.FINISHED
    taskstate.signal()
