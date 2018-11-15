import enum
import weakref
import os
import time
import numpy as np
from sklearn.metrics import r2_score
import pickle

import renom as rm
from renom.optimizer import Adam
from renom.cuda import set_cuda_active, release_mem_pool, use_device
from renom.utility.distributor.distributor import NdarrayDistributor

from renom_rg.server import (C_GCNN, Kernel_GCNN, DBSCAN_GCNN, DB_DIR_TRAINED_WEIGHT, DATASRC_DIR)

from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.feature_graph import get_corr_graph, get_kernel_graph, get_dbscan_graph
from . import db

class RunningState(enum.Enum):
    TRAINING = 0
    VALIDATING = 1
    PREDICTING = 2
    STARTING = 3
    STOPPING = 4


class TaskState:

    tasks = weakref.WeakValueDictionary()  # Mapping of {model.id: TaskState()}

    @classmethod
    def add_task(cls, model):
        ret = TaskState()
        cls.tasks[model.id] = ret
        return ret

    def __init__(self):
        self.error_msgs = []
        self.state = RunningState.STARTING
        self.canceled = False
        self.nth_epoch = -1
        self.nth_batch = -1
        self.train_loss = -1
        self.total_epoch = -1
        self.total_batch = -1
        self.algorithm = -1


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
        for i in range(num_bin):
            true_data_index = np.logical_and(bins[i] < d, d < bins[i + 1])
            pred_data_in_bin = pred_data[j][true_data_index]

            m = np.mean(pred_data_in_bin)
            sd = np.sqrt(np.sum((pred_data_in_bin - m)**2) / len(pred_data_in_bin))
            c = np.array([m - sd * 2, m - sd, m, m + sd, m + sd * 2]).reshape(1, -1)

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
        return _train(session, taskstate, model_id)
    finally:
        session.commit()

def _train(session, taskstate, model_id):
    modeldef = session.query(db.Model).get(model_id)

    total_batch = 0
    best_loss = None
    train_loss_list = []
    valid_loss_list = []
    valid_predicted = []
    valid_true = []

    with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
        data = pickle.load(f)

    X, y = split_target(np.array(data), pickle.loads(modeldef.dataset.target_column_ids))

    X_train = X[pickle.loads(modeldef.dataset.train_index)]
    X_valid = X[pickle.loads(modeldef.dataset.valid_index)]
    y_train = y[pickle.loads(modeldef.dataset.train_index)]
    y_valid = y[pickle.loads(modeldef.dataset.valid_index)]
    valid_true = y_valid

    taskstate.algorithm = modeldef.algorithm
    algorithm_params = pickle.loads(modeldef.algorithm_params)
    if modeldef.algorithm == C_GCNN:
        feature_graph = get_corr_graph(X_train, algorithm_params["num_neighbors"])
    elif modeldef.algorithm == Kernel_GCNN:
        feature_graph = get_kernel_graph(X_train, algorithm_params["num_neighbors"], 0.01)
    elif modeldef.algorithm == DBSCAN_GCNN:
        feature_graph = get_dbscan_graph(X_train, algorithm_params["num_neighbors"])
    else:
        raise ValueError("{} is not supported algorithm id.".format(modeldef.algorithm))

    model = GCNet(feature_graph, num_target=y_train.shape[1],
                  fc_unit=algorithm_params["fc_unit"],
                  neighbors=algorithm_params["num_neighbors"],
                  channels=algorithm_params["channels"])

    # update network params for prediciton
    algorithm_params["feature_graph"] = feature_graph.tolist()
    algorithm_params["num_target"] = y_train.shape[1]
    modeldef.algorithm_params = pickle.dumps(algorithm_params)

    filename = '{}.h5'.format(int(time.time()))
    optimizer = Adam()

    taskstate.state = RunningState.TRAINING
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

            index = perm[j * modeldef.batch_size:(j + 1) * modeldef.batch_size]
            train_batch_x = X_train[index].reshape(-1, 1, X_train.shape[1], 1)
            train_batch_y = y_train[index]

            # Loss function
            model.set_models(inference=False)
            with model.train():
                train_predicted = model(train_batch_x)
                batch_loss = rm.mse(train_predicted, train_batch_y)
                taskstate.train_loss = batch_loss.tolist()

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

        train_loss = loss / (N // modeldef.batch_size)
        train_loss_list.append(train_loss)

        # Validation
        taskstate.running_state = RunningState.VALIDATING

        model.set_models(inference=True)
        N = X_valid.shape[0]

        valid_predicted = model(X_valid.reshape(-1, 1, X_valid.shape[1], 1))
        valid_loss = float(rm.mse(valid_predicted, y_valid))
        valid_loss_list.append(valid_loss)

        modeldef.train_loss_list = pickle.dumps(train_loss_list)
        modeldef.valid_loss_list = pickle.dumps(valid_loss_list)
        modeldef.valid_predicted = pickle.dumps(valid_predicted.T.tolist())
        modeldef.valid_true = pickle.dumps(valid_true.T.tolist())

        sampled_train_pred = train_predicted_list
        sampled_train_true = train_true_list

        modeldef.sampled_train_pred = pickle.dumps(sampled_train_pred.T.tolist())
        modeldef.sampled_train_true = pickle.dumps(sampled_train_true.T.tolist())

        # calc train data confidence area
        confidence_data_list = calc_confidence_area(train_true_list.T, train_predicted_list.T)
        modeldef.confidence_data = pickle.dumps(confidence_data_list.tolist())

        session.add(modeldef)
        session.commit()

        print("epoch: {}, valid_loss: {}".format(e, valid_loss))

        # update best loss model info
        if best_loss is None or best_loss > valid_loss:
            model.save(os.path.join(DB_DIR_TRAINED_WEIGHT, filename))

            modeldef.best_epoch = e
            modeldef.best_epoch_valid_loss = valid_loss
            modeldef.best_epoch_rmse = float(np.sqrt(valid_loss))
            modeldef.best_epoch_max_abs_error = float(np.max(np.abs(y_valid - valid_predicted)))
            modeldef.r2_score = float(r2_score(y_valid, valid_predicted))
            modeldef.weight = filename

            session.add(modeldef)
            session.commit()

            best_loss = valid_loss


class TrainThread(object):
    def __init__(self):
        pass

    def train(self, taskstate, model_id):
        self.model_id = model_id
        self.taskstate = taskstate
        train(taskstate, model_id)
