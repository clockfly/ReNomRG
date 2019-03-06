import pickle
from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.feature_graph import get_corr_graph

def create_model(algorithm_params):
    model = GCNet(list(algorithm_params["feature_graph"]),
                  num_target=int(algorithm_params["num_target"]),
                  fc_unit=[int(u) for u in algorithm_params["fc_unit"]],
                  neighbors=int(algorithm_params["num_neighbors"]),
                  channels=[int(u) for u in algorithm_params["channels"]])
    return model
