import math
import itertools
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize


def cdist(A, B):
    """ Distance matrix."""
    return distance.cdist(A, B)


def get_corr_graph(X, neighbors, explanatory_column_ids=[]):
    """ Get correlation feature graph.

    Args:
        neighbors (int): Number of neighbors.
        explanatory_column_ids(list): List of explanatory_column_ids.

    Returns:
        (array): This returns matrix of neighbrs indexes per variables.
    """
    if explanatory_column_ids and len(explanatory_column_ids) == 1:
        corr_mat = np.array([[1]])
    else:
        corr_mat = np.array(normalize(np.abs(np.corrcoef(X.T)), norm='l1', axis=1))

    feature_graph = np.argsort(corr_mat, 1)[:, -neighbors:]
    return feature_graph


def get_kernel_graph(X, neighbors, gamma):
    """ Get kernel feature graph.

    Args:
        neighbors (int): Number of neighbors.
        gamma (float): Bandwidth.

    Returns:
        (array): This returns matrix of neighbrs indexes per variables.
    """
    X_t = X.T
    krbf = np.zeros((X.shape[1], X.shape[1]))

    for index in itertools.combinations_with_replacement(range(X.shape[1]), 2):
        d = math.exp(-(np.linalg.norm(X_t[index[0]] - X_t[index[1]])**2) / gamma**2)
        krbf[index[0], index[1]] = d
        if index[0] != index[1]:
            krbf[index[1], index[0]] = d

    feature_graph = np.argsort(krbf, 1)[:, -neighbors:]
    return feature_graph


def get_dbscan_graph(X, neighbors):
    """ Get DBSCAN feature graph.

    Args:
        neighbors (int): Number of neighbors.

    Returns:
        (array): This returns matrix of neighbrs indexes per variables.
    """
    X_t = X.T
    dist_mat = cdist(X_t, X_t)
    feature_graph = np.argsort(dist_mat, 1)[:, :neighbors]
    return feature_graph
