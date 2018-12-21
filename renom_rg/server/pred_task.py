import os
import pickle
import numpy as np

from renom_rg.server import DB_DIR_TRAINED_WEIGHT, USER_DEFINED
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
    else:
        model = GCNet(np.array(algorithm_params["feature_graph"]), num_target=algorithm_params["num_target"],
                      fc_unit=algorithm_params["fc_unit"],
                      neighbors=algorithm_params["num_neighbors"],
                      channels=algorithm_params["channels"])

    path = os.path.join(DB_DIR_TRAINED_WEIGHT, modeldef.weight)
    model.load(path)

    model.set_models(inference=True)
    pred = model(data.reshape(-1, 1, data.shape[1], 1))
    return pred
