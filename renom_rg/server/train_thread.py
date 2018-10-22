import os
import time
import numpy as np
import traceback
from sklearn.metrics import r2_score
from threading import Event, Semaphore
try:
    import _pickle as pickle
except:
    import cPickle as pickle

import renom as rm
from renom.optimizer import Adam
from renom.cuda import set_cuda_active, release_mem_pool, use_device
from renom.utility.distributor.distributor import NdarrayDistributor

from renom_rg.server import GPU_NUM, STATE_RUNNING, RUN_STATE_TRAINING, RUN_STATE_VALIDATING, RUN_STATE_STARTING, RUN_STATE_STOPPING, C_GCNN, Kernel_GCNN, DBSCAN_GCNN, DB_DIR_TRAINED_WEIGHT, DATASRC_DIR
from renom_rg.api.regression.gcnn import GCNet
from renom_rg.server.storage import storage


def split_target(data, target_column_id):
    X = data[:, np.arange(data.shape[1]) != target_column_id]
    y = data[:, target_column_id].reshape(-1, 1)
    return X, y


class TrainThread(object):
    gpu_resource = Semaphore(GPU_NUM or 1)
    gpus = set(range(GPU_NUM or 1))

    def __init__(self, model_id, dataset_id, algorithm,
                 algorithm_params, batch_size, epoch):

        # Model will be created in __call__ function.
        self.model = None
        self.model_id = model_id

        # State of thread.
        # The variable _running_state has setter and getter.
        self._running_state = RUN_STATE_STARTING
        self.nth_batch = 0
        self.total_batch = 0
        self.last_batch_loss = 0
        self.nth_epoch = 0
        self.best_loss = None
        self.train_loss_list = []
        self.valid_loss_list = []

        # Error message caused in thread.
        self.error_msg = None

        # Train hyperparameters
        self.dataset_id
        self.total_epoch = epoch
        self.batch_size = batch_size
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params

        self.stop_event = Event()

    @property
    def running_state(self):
        return self._running_state

    @running_state.setter
    def running_state(self, state):
        """
        If thread's state becomes RUN_STATE_STOPPING once,
        state will never be changed.
        """
        if self._running_state != RUN_STATE_STOPPING:
            self._running_state = state

    def __call__(self):
        set_cuda_active(True)
        with self.gpu_resource:
            self._gpu = self.gpus.pop()
            try:
                with use_device(self._gpu):
                    return self._exec()
            finally:
                self.gpus.add(self._gpu)

    def _exec(self):
        # This func works as thread.
        try:
            # Algorithm and model preparation.
            # Pretrained weights are must be prepared.
            # This have to be done in thread.
            if self.algorithm == C_GCNN:
                # self.feature_mat = feature_mat()
                pass
            elif self.algorithm == Kernel_GCNN:
                # self.feature_mat = feature_mat()
                pass
            elif self.algorithm == DBSCAN_GCNN:
                # self.feature_mat = feature_mat()
                pass
            else:
                self.error_msg = "{} is not supported algorithm id.".format(self.algorithm)
            self.model = GCNet()

            self.model.set_gpu(self._gpu)
            release_mem_pool()
            filename = '{}.h5'.format(int(time.time()))

            with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
                data = pickle.load(f)
            X, y = split_target(np.array(data), self.target_column_id)
            X_train = X[self.train_index]
            X_valid = X[self.valid_index]
            y_train = y[self.train_index]
            y_test = y[self.valid_index]

            optimizer = Adam()
            storage.update_model_state(self.model_id, STATE_RUNNING)
            self.running_state = RUN_STATE_TRAINING
            for e in range(self.epoch):
                self.nth_epoch = e
                N = X_train.shape[0]
                perm = np.random.permutation(N)
                loss = 0
                self.total_batch = N // self.batch_size
                for j in range(self.total_batch):
                    self.nth_batch = j
                    index = perm[j * self.batch_size:(j + 1) * self.batch_size]
                    train_batch_x = X_train[index].reshape(-1, 1, X_train.shape[1], 1)
                    train_batch_y = y_train[index]

                    # Loss function
                    self.model.set_models(inference=False)
                    with self.model.train():
                        l = rm.mse(self.model(train_batch_x), train_batch_y)
                        self.last_batch_loss = l
                    # Back propagation
                    grad = l.grad()
                    # Update
                    grad.update(optimizer)
                    loss += l.as_ndarray()

                train_loss = loss / (N // self.batch_size)
                self.train_loss_list.append(train_loss)

                # Validation
                self.running_state = RUN_STATE_VALIDATING
                self.model.set_models(inference=True)
                N = X_valid.shape[0]

                pred = self.model(X_valid.reshape(-1, 1, X_valid.shape[1], 1))
                valid_loss = rm.mse(pred, y_test)
                self.valid_loss_list.append(valid_loss)

                # calc evaluation
                if self.best_loss is None or self.best_loss > valid_loss:
                    self.model.save(os.path.join(DB_DIR_TRAINED_WEIGHT, filename))

                    self.best_loss = valid_loss
                    rmse = np.sqrt(valid_loss)
                    max_abs_error = np.max(np.abs(y_test - pred))
                    r2 = r2_score(y_test, pred)
                    storage.update_best_epoch(self.model_id, e, valid_loss,
                                              rmse, max_abs_error, r2, filename)

        except Exception as e:
            traceback.print_exc()
            self.error_msg = str(e)
            self.model = None
            release_mem_pool()

    def stop(self):
        # Thread can be canceled only if it have not been started.
        # This method is for stopping running thread.
        self.stop_event.set()
        self.running_state = RUN_STATE_STOPPING

    def is_stopped(self):
        return self.stop_event.is_set()
