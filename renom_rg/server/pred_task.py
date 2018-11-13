import os
import pickle
import numpy as np

from renom_rg.server import (STATE_RUNNING, RUN_STATE_TRAINING,
                             RUN_STATE_VALIDATING, RUN_STATE_STARTING, RUN_STATE_STOPPING, C_GCNN,
                             Kernel_GCNN, DBSCAN_GCNN, DB_DIR_TRAINED_WEIGHT, DATASRC_DIR)

from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.feature_graph import get_corr_graph, get_kernel_graph, get_dbscan_graph
from . import db

def prediction(model_id, data):
    session = db.session()
    try:
        return _prediction(session, model_id, data)
    finally:
        session.commit()

def _prediction(session, model_id, data):
    modeldef = session.query(db.Model).get(model_id)

    # Algorithm and model preparation.
    # Pretrained weights are must be prepared.
    # This have to be done in thread.

    algorithm_params = pickle.loads(modeldef.algorithm_params)

    model = GCNet(np.array(algorithm_params["feature_graph"]), num_target=algorithm_params["num_target"],
                  fc_unit=algorithm_params["fc_unit"],
                  neighbors=algorithm_params["num_neighbors"],
                  channels=algorithm_params["channels"])
    path = os.path.join(DB_DIR_TRAINED_WEIGHT, modeldef.weight)
    model.load(path)

    model.set_models(inference=True)
    pred = model(data.reshape(-1, 1, data.shape[1], 1))
    return pred
