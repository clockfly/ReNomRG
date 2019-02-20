import os
import pickle
import numpy as np

from renom_rg.server import DB_DIR_TRAINED_WEIGHT, DB_DIR_ML_MODELS, USER_DEFINED, RANDOM_FOREST
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
    elif modeldef.algorithm == RANDOM_FOREST:
        mp_path = os.path.join(DB_DIR_ML_MODELS, modeldef.model_pickle)
        with open(mp_path, mode='rb') as f:
            model = pickle.load(f)
    else:
        model = GCNet(np.array(algorithm_params["feature_graph"]), num_target=algorithm_params["num_target"],
                      fc_unit=algorithm_params["fc_unit"],
                      neighbors=algorithm_params["num_neighbors"],
                      channels=algorithm_params["channels"])

    if modeldef.algorithm == RANDOM_FOREST:
        pred = model.predict(data)
        if len(pred.shape) == 1:
            pred = pred.reshape(-1, 1)
    else:
        w_path = os.path.join(DB_DIR_TRAINED_WEIGHT, modeldef.weight)
        model.load(w_path)
        model.set_models(inference=True)
        pred = model(data.reshape(-1, 1, data.shape[1], 1))

    return pred
