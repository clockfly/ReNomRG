import math
import itertools
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize


def cdist(A, B):
    """ Distance matrix."""
    return distance.cdist(A, B)


def get_corr_graph(X, neighbors):
    """ Get correlation feature graph.

    Args:
        neighbors: Number of neighbors.

    Returns:
        (Matrix): This returns matrix of neighbrs indexes per variables.
    """
    corr_mat = np.array(normalize(np.abs(np.corrcoef(X.T)), norm='l1', axis=1))
    feature_graph = np.argsort(corr_mat, 1)[:, -neighbors:]
    return feature_graph


def get_kernel_graph(X, neighbors, gamma):
    """ Get kernel feature graph.

    Args:
        neighbors: Number of neighbors.
        gamma: Bandwidth.

    Returns:
        (Matrix): This returns matrix of neighbrs indexes per variables.
    """
    X_t = X.T
    krbf = np.zeros((X.shape[1], X.shape[1]))

    for i in range(X.shape[1]):
        for j in range(X.shape[1]):
            krbf[i, j] = math.exp(-(np.linalg.norm(X_t[i] - X_t[j]) ** 2) / gamma ** 2)
    feature_graph = np.argsort(krbf, 1)[:, -neighbors:]
    return feature_graph


def get_dbscan_graph(X, neighbors):
    """ Get DBSCAN feature graph.

    Args:
        neighbors: Number of neighbors.

    Returns:
        (Matrix): This returns matrix of neighbrs indexes per variables.
    """
    X_t = X.T
    dist_mat = cdist(X_t, X_t)
    feature_graph = np.argsort(dist_mat)[:, :neighbors]
    return feature_graph
