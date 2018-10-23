import datetime
import os
import sys
import sqlite3
import json
from renom_rg.server import DB_DIR
try:
    import _pickle as pickle
except:
    import cPickle as pickle

unicode = "ascii"

def pickle_dump(obj):
    return pickle.dumps(obj)


def pickle_load(pickled_obj):
    if sys.version_info.major == 2:
        if isinstance(pickled_obj, unicode):
            pickled_obj = pickled_obj.encode()
        return pickle.loads(pickled_obj)
    else:
        return pickle.loads(pickled_obj, encoding='ascii')


class Storage:
    def __init__(self):
        dbname = os.path.join(DB_DIR, 'storage.db')
        self.db = sqlite3.connect(dbname,
                                  check_same_thread=False,
                                  detect_types=sqlite3.PARSE_DECLTYPES,
                                  isolation_level=None)

        self.db.execute('PRAGMA journal_mode = WAL')
        self.db.execute('PRAGMA foreign_keys = ON')
        self._init_db()

    def cursor(self):
        return self.db.cursor()

    def _init_db(self):
        c = self.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS dataset_def
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             description TEXT,
             target_column_id INTEGER,
             labels BLOB NOT NULL,
             train_ratio NUMBER,
             train_index BLOB,
             valid_index BLOB,
             created TIMESTAMP NOT NULL,
             updated TIMESTAMP NOT NULL)
            """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS model
            (model_id INTEGER PRIMARY KEY AUTOINCREMENT,
             dataset_id NOT NULL REFERENCES dataset_def(id) ON DELETE CASCADE,
             state INTEGER NOT NULL DEFAULT 0,
             algorithm INTEGER NOT NULL DEFAULT 0,
             algorithm_params BLOB,
             batch_size INTEGER NOT NULL,
             epoch INTEGER NOT NULL,
             train_loss_list BLOB,
             valid_loss_list BLOB,
             best_epoch INTEGER,
             best_epoch_valid_loss NUMBER,
             best_epoch_rmse NUMBER,
             best_epoch_max_abs_error NUMBER,
             best_epoch_r2 NUMBER,
             valid_predicted BLOB,
             weight TEXT,
             deployed INTEGER NOT NULL DEFAULT 0,
             created TIMESTAMP,
             updated TIMESTAMP)
        """)

    def now(self):
        return datetime.datetime.now()

    def register_model(self, dataset_id, algorithm, algorithm_params, batch_size, epoch):
        with self.db:
            c = self.cursor()
            now = self.now()
            dumped_algorithm_params = pickle_dump(algorithm_params)
            dumped_empty_list = pickle_dump([])
            c.execute("""
                INSERT INTO
                    model(dataset_id, algorithm, algorithm_params,
                          batch_size, epoch, train_loss_list, valid_loss_list,
                          valid_predicted, created, updated)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (dataset_id, algorithm, dumped_algorithm_params,
                      batch_size, epoch, dumped_empty_list,
                      dumped_empty_list, dumped_empty_list, now, now))
            return c.lastrowid

    def update_model_state(self, model_id, state):
        with self.db:
            c = self.cursor()
            now = self.now()
            c.execute("""
                UPDATE model
                SET
                    state=?, updated=?
                WHERE
                    model_id=?
                """, (state, now, model_id))
            return c.lastrowid

    def update_model_deploy(self, model_id):
        with self.db:
            c = self.cursor()
            now = self.now()
            # clear deployed model
            c.execute("""
                UPDATE model
                SET
                    deployed=0, updated=?
                """, (now,))
            # set deployed model deployed=1
            c.execute("""
                UPDATE model
                SET
                    deployed=1, updated=?
                WHERE
                    model_id=?
                """, (now, model_id))
            return c.lastrowid

    def update_model_undeploy(self, model_id):
        with self.db:
            c = self.cursor()
            now = self.now()
            # clear deployed model
            c.execute("""
                UPDATE model
                SET
                    deployed=0, updated=?
                """, (now,))
            return c.lastrowid

    def update_best_epoch(self, model_id, nth_epoch, valid_loss,
                          rmse, max_abs_error, r2_score, filename):
        with self.db:
            c = self.cursor()
            now = self.now()
            c.execute("""
                UPDATE model
                SET
                    best_epoch=?, best_epoch_valid_loss=?,
                    best_epoch_rmse=?, best_epoch_max_abs_error=?,
                    best_epoch_r2=?, weight=?, updated=?
                WHERE
                    model_id=?
                """, (nth_epoch, valid_loss, rmse, max_abs_error,
                      r2_score, filename, now, model_id))
            return c.lastrowid

    def update_weight(self, model_id, weight):
        with self.db:
            c = self.cursor()
            now = self.now()
            c.execute("""
                UPDATE model
                SET
                    weight=?, updated=?
                WHERE
                    model_id=?
                """, (weight, now, model_id))
            return c.lastrowid

    def fetch_models(self):
        with self.db:
            c = self.cursor()
            c.execute("""
                SELECT model_id, state, algorithm,
                       best_epoch_valid_loss, best_epoch_rmse,
                       best_epoch_max_abs_error, best_epoch_r2,
                       deployed
                FROM model
                WHERE state<3
                ORDER BY model_id DESC
                """)

            ret = []
            for index, data in enumerate(c):
                ret.append({
                    "model_id": data[0],
                    "state": data[1],
                    "algorithm": data[2],
                    "best_epoch_valid_loss": data[3],
                    "best_epoch_rmse": data[4],
                    "best_epoch_max_abs_error": data[5],
                    "best_epoch_r2": data[6],
                    "deployed": data[7]
                })
            return ret

    def fetch_model(self, model_id):
        with self.db:
            c = self.cursor()
            c.execute("""
                SELECT dataset_id, state, algorithm, algorithm_params,
                       batch_size, epoch, train_loss_list,
                       valid_loss_list, best_epoch_valid_loss,
                       best_epoch_rmse, best_epoch_max_abs_error,
                       best_epoch_r2, valid_predicted, deployed,
                       weight
                FROM model WHERE model_id=?
                """, (model_id,))

            for index, data in enumerate(c):
                ret = {
                    "model_id": model_id,
                    "dataset_id": data[0],
                    "state": data[1],
                    "algorithm": data[2],
                    "algorithm_params": pickle_load(data[3]),
                    "batch_size": data[4],
                    "epoch": data[5],
                    "train_loss_list": pickle_load(data[6]),
                    "valid_loss_list": pickle_load(data[7]),
                    "best_epoch_valid_loss": data[8],
                    "best_epoch_rmse": data[9],
                    "best_epoch_max_abs_error": data[10],
                    "best_epoch_r2": data[11],
                    "valid_predicted": pickle_load(data[12]),
                    "deployed": data[13],
                    "weight": data[14]
                }
                return ret

    def register_dataset(self, name, description,
                         target_column_id, labels,
                         train_ratio, train_index, valid_index):
        with self.db:
            c = self.cursor()
            now = self.now()
            dumped_train_index = pickle_dump(train_index)
            dumped_valid_index = pickle_dump(valid_index)
            dumped_labels = pickle_dump(labels)
            c.execute("""
                INSERT INTO
                    dataset_def(name, description,
                                target_column_id, labels,
                                train_ratio, train_index,
                                valid_index, created, updated)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, description, target_column_id,
                      dumped_labels, train_ratio, dumped_train_index,
                      dumped_valid_index, now, now))
            return c.lastrowid

    def fetch_datasets(self):
        with self.db:
            c = self.cursor()
            c.execute("""
                SELECT id, name, train_ratio, created
                FROM dataset_def
                """)

            ret = []
            for index, data in enumerate(c):
                ret.append({
                    "dataset_id": data[0],
                    "name": data[1],
                    "train_ratio": data[2],
                    "created": data[3].strftime('%Y/%m/%d')
                })
            return ret

    def fetch_dataset(self, dataset_id):
        with self.db:
            c = self.cursor()
            c.execute("""
                SELECT id, name, description,
                       target_column_id, labels,
                       train_ratio, train_index,
                       valid_index, created
                FROM dataset_def
                """)

            for index, data in enumerate(c):
                ret = {
                    "dataset_id": data[0],
                    "name": data[1],
                    "description": data[2],
                    "target_column_id": data[3],
                    "labels": pickle_load(data[4]),
                    "train_ratio": data[5],
                    "train_index": pickle_load(data[6]),
                    "valid_index": pickle_load(data[7]),
                    "created": data[8].strftime('%Y/%m/%d')
                }
                return ret

    def delete_dataset(self, dataset_id):
        with self.db:
            c = self.cursor()
            c.execute("""
                DELETE FROM dataset_def
                WHERE dataset_id=?
                """, (dataset_id,))


global storage
storage = Storage()
