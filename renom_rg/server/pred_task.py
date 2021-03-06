"""
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
"""

import os
import pickle
import numpy as np

import renom as rm
from renom_rg.server import DB_DIR_TRAINED_WEIGHT, DB_DIR_ML_MODELS, USER_DEFINED, RANDOM_FOREST, XGBOOST
from renom_rg.server.custom_util import _load_usermodel

from renom_rg.api.regression.gcnn import GCNet
from . import db


def prediction(model_id, data):
    session = db.session()
    try:
        return _prediction(session, model_id, data)
    finally:
        session.commit()


def _prediction(session, model_id, data):
    modeldef = session.query(db.Model).get(model_id)

    algorithm_params = pickle.loads(modeldef.algorithm_params)

    if modeldef.algorithm == USER_DEFINED:
        model = _load_usermodel(algorithm_params)
    elif modeldef.algorithm in [RANDOM_FOREST, XGBOOST]:
        mp_path = os.path.join(DB_DIR_ML_MODELS, modeldef.model_pickle)
        with open(mp_path, mode='rb') as f:
            model = pickle.load(f)
    else:
        model = GCNet(np.array(algorithm_params["feature_graph"]), num_target=algorithm_params["num_target"],
                      fc_unit=algorithm_params["fc_unit"],
                      neighbors=algorithm_params["num_neighbors"],
                      channels=algorithm_params["channels"])

    pred_list = None
    if modeldef.algorithm in [RANDOM_FOREST, XGBOOST]:
        pred_list = model.predict(data)
        if len(pred_list.shape) == 1:
            pred_list = pred_list.reshape(-1, 1)
    else:
        w_path = os.path.join(DB_DIR_TRAINED_WEIGHT, modeldef.weight)
        model.load(w_path)
        model.set_models(inference=True)

        d_N = data.shape[0]
        total_batch = d_N // modeldef.batch_size
        if total_batch != d_N / modeldef.batch_size:
            total_batch = total_batch + 1
        for j in range(total_batch):
            index = range(d_N)[j * modeldef.batch_size:(j + 1) * modeldef.batch_size]
            pred = model(data[index].reshape(-1, 1, data.shape[1], 1))
            if rm.is_cuda_active():
                pred = pred.as_ndarray()

            if pred_list is None:
                pred_list = pred
            else:
                pred_list = np.concatenate([pred_list, pred])

    return pred_list
