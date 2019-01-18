import requests
import os
from renom_rg.server import (C_GCNN, Kernel_GCNN, DBSCAN_GCNN, USER_DEFINED,
                             DB_DIR_TRAINED_WEIGHT, DATASRC_DIR, SCRIPT_DIR)
from renom_rg.server.custom_util import _load_usermodel
from renom_rg.api.regression.gcnn import GCNet
from renom_rg.api.utility.download import download

class Regressor(object):
    """ This class allows you to pull model which trained on ReNomRG GUI Tool.

    Args:
        url (string): The url ReNomRG server running.
        port (string): The port number ReNomRG server running.
    """

    def __init__(self, url="http://localhost", port='8080'):
        self._url = url
        self._port = port
        self._model = None
        self._alg_name = None
        self._model_info = {}

    def __call__(self, x):
        assert self._model is not None, "Please pull trained weight first."
        return self._model(x)

    def pull(self):
        """Pull trained weight from ReNomRG server.
        Trained weight will be downloaded into current directory.

        Example:
            >>> from renom_rg.api.inference.regressor import Regressor
            >>> regressor = Regressor()
            >>> regressor.pull()

        """
        url = self._url + ':' + self._port
        download_weight_api = "/api/renom_rg/deployed_model"
        download_param_api = "/api/renom_rg/deployed_model_info"
        download_weight_api = url + download_weight_api
        download_param_api = url + download_param_api

        ret = requests.get(download_param_api).json()
        params = ret["algorithm_params"]
        filename = ret["weight"]
        if not os.path.exists(filename):
            download(download_weight_api, filename)

        if ret["algorithm"] == USER_DEFINED:
            self._model = _load_usermodel(params)
        else:
            if ret["algorithm"] == C_GCNN:
                self._alg_name = "C_GCNN"
            elif ret["algorithm"] == Kernel_GCNN:
                self._alg_name = "Kernel_GCNN"
            elif ret["algorithm"] == DBSCAN_GCNN:
                self._alg_name = "DBSCAN_GCNN"

            self._model = GCNet(list(params["feature_graph"]),
                                num_target=int(params["num_target"]),
                                fc_unit=[int(u) for u in params["fc_unit"]],
                                neighbors=int(params["num_neighbors"]),
                                channels=[int(u) for u in params["channels"]])

        self._model.load(filename)
        self._model_info = {
            "model_id": ret["model_id"],
            "dataset_id": ret["dataset_id"],
            "algorithm": self._alg_name,
            "algorithm_params": params
        }

    def predict(self, X):
        """
        Perform prediction to given data.

        Args:
            X: Input data for prediction.

        Example:
            >>> from renom_rg.api.inference.detector import Detector
            >>> detector = Detector()
            >>> detector.pull()
            >>> print(detector.predict(X))
            [[],
             [],
             :
             :
             :
             []]

        """
        assert self._model
        return self._model.predict(X)

    @property
    def model_info(self):
        """This function returns information of pulled model.

        Example:
            >>> from renom_img.api.inference.detector import Detector
            >>> detector = Detector()
            >>> detector.pull()
            >>> print(detector.model_info)
        """
        return self._model_info
