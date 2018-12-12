import pickle
from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.feature_graph import get_corr_graph

def create_model(modeldef, algorithm_params, X_train, X_valid, y_train, y_valid):

    num_neighbors = int(algorithm_params["num_neighbors"])
    feature_graph = get_corr_graph(X_train, num_neighbors)

    model = GCNet(feature_graph, num_target=y_train.shape[1],
                  fc_unit=[int(u) for u in algorithm_params["fc_unit"]],
                  neighbors=num_neighbors,
                  channels=[int(u) for u in algorithm_params["channels"]])
    return model
