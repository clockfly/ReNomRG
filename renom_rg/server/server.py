# coding: utf-8

import argparse
import os
import json
import pkg_resources
import mimetypes
import posixpath
import traceback
import pandas as pd
import numpy as np
try:
    import _pickle as pickle
except:
    import cPickle as pickle


from bottle import HTTPResponse, default_app, route, request, error
from concurrent.futures import ThreadPoolExecutor as Executor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import CancelledError
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

import renom as rm
from renom.cuda import release_mem_pool

from renom_rg.server import MAX_THREAD_NUM, DATASRC_DIR, STATE_RESERVED, STATE_RUNNING, STATE_FINISHED, STATE_DELETED
from renom_rg.server import wsgi_server
from renom_rg.server.train_thread import TrainThread
from renom_rg.server.storage import storage
from . import *
from . import db


def create_response(body):
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r


def strip_path(filename):
    if os.path.isabs(filename):
        raise ValueError('Invalid path')
    if '..' in filename:
        raise ValueError('Invalid path')
    if ':' in filename:
        raise ValueError('Invalid path')

    filename = filename.strip().strip('./\\')
    return filename


def _get_resource(path, filename):
    filename = strip_path(filename)
    body = pkg_resources.resource_string(__name__, posixpath.join('.build', path, filename))

    headers = {}
    mimetype, encoding = mimetypes.guess_type(filename)
    if mimetype:
        headers['Content-Type'] = mimetype
    if encoding:
        headers['encoding'] = encoding
    return HTTPResponse(body, **headers)


def create_error_body(e):
    return json.dumps({"error_msg": e})


def split_target(data, target_column_id):
    X = data.iloc[:, np.arange(data.shape[1]) != target_column_id]
    y = data.iloc[:, target_column_id]
    return X, y


@route("/")
def index():
    return _get_resource('', 'index.html')


@route("/static/<file_name:re:.+>")
def static(file_name):
    return _get_resource('static', file_name)


@route("/css/<file_name:path>")
def css(file_name):
    return _get_resource('static/css/', file_name)


@error(404)
def error404(error):
    body = json.dumps({"error_msg": "Page Not Found"})
    ret = create_response(body)
    return ret


@route('/api/renom_rg/datasets', method='GET')
def get_datasets():
    try:
        datasets = storage.fetch_datasets()
        body = json.dumps({"datasets": datasets})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets/labels', method='GET')
def get_labels():
    try:
        with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
            data = pickle.load(f)
        body = json.dumps({"labels": list(data.columns)})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets/<dataset_id:int>', method='GET')
def get_dataset(dataset_id):
    try:
        dataset = storage.fetch_dataset(dataset_id)
        body = json.dumps({"dataset": dataset})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets/confirm', method='POST')
def confirm_dataset():
    try:
        target_column_id = int(request.params.target_column_id)
        train_ratio = float(request.params.train_ratio)

        with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
            data = pickle.load(f)
        X, y = split_target(data, target_column_id)
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=(1 - train_ratio))

        body = json.dumps({
            "train_count": y_train.shape[0],
            "valid_count": y_valid.shape[0],
            "target_train": y_train.values.tolist(),
            "target_valid": y_valid.values.tolist(),
            "train_index": np.array(y_train.index).tolist(),
            "valid_index": np.array(y_valid.index).tolist()
        })
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets', method='POST')
def create_dataset():
    try:
        name = request.params.name
        description = request.params.description
        target_column_id = int(request.params.target_column_id)
        labels = json.loads(request.params.labels)
        train_ratio = float(request.params.train_ratio)
        train_index = json.loads(request.params.train_index)
        valid_index = json.loads(request.params.valid_index)

        storage.register_dataset(name, description, target_column_id,
                                 labels, train_ratio, train_index, valid_index)
        body = json.dumps({})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets/<dataset_id:int>', method='DELETE')
def delete_dataset(dataset_id):
    try:
        storage.delete_dataset(dataset_id)
        body = json.dumps({})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models", method="GET")
def get_models():
    try:
        models = storage.fetch_models()
        body = json.dumps({"models": models})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models/<model_id:int>", method="GET")
def get_model(model_id):
    try:
        model = storage.fetch_model(model_id)
        body = json.dumps({"model": model})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models", method="POST")
def create_model():
    try:
        dataset_id = int(request.params.dataset_id)
        algorithm = int(request.params.algorithm)
        algorithm_params = json.loads(request.params.algorithm_params)
        batch_size = int(request.params.batch_size)
        epoch = int(request.params.epoch)

        model_id = storage.register_model(dataset_id, algorithm, algorithm_params,
                                          batch_size, epoch)

        body = json.dumps({"model_id": model_id})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models/<model_id:int>", method="DELETE")
def delete_model(model_id):
    try:
        storage.update_model_state(model_id, STATE_DELETED)
        body = {}
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models/<model_id:int>/deploy", method="POST")
def deploy_model(model_id):
    try:
        model_id = storage.update_model_deploy(model_id)
        body = json.dumps({"model_id": model_id})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models/<model_id:int>/undeploy", method="POST")
def undeploy_model(model_id):
    try:
        storage.update_model_deploy(model_id)
        body = json.dumps({"model_id": model_id})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


@route("/api/renom_rg/models/<model_id:int>/train", method="GET")
def train_model(model_id):
    try:
        # run train thread
        model = storage.fetch_model(model_id)
        dataset = storage.fetch_dataset(model['dataset_id'])
        th = TrainThread(model_id,
                         model['dataset_id'],
                         model['algorithm'],
                         model['algorithm_params'],
                         model["batch_size"],
                         model['epoch'],
                         dataset['train_index'],
                         dataset['valid_index'],
                         dataset['target_column_id'])
        ft = executor.submit(th)
        train_thread_pool[model_id] = [ft, th]

        try:
            # This will wait for end of thread.
            ft.result()
            ft.cancel()
        except CancelledError as ce:
            # If the model is deleted or stopped,
            # program reaches here.
            pass

        error_msg = th.error_msg
        del train_thread_pool[model_id]
        ft = None
        th = None

        model = storage.fetch_model(model_id)
        if model['state'] != STATE_DELETED:
            storage.update_model_state(model_id, STATE_FINISHED)
        release_mem_pool()

        if error_msg is not None:
            body = json.dumps({"error_msg": error_msg})
            ret = create_response(body)
            return ret
        body = json.dumps({"dummy": ""})
    except Exception as e:
        release_mem_pool()
        traceback.print_exc()
        body = json.dumps({"error_msg": e.args[0]})
    ret = create_response(body)
    return ret



@route("/api/renom_rg/models/<model_id:int>/predict", method="GET")
def predict_model(model_id):
    try:
        # run prediction thread
        body = json.dumps({})
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


def _init_cuda():
    try:
        import renom.cuda
        if renom.cuda.has_cuda():
            MAX_THREAD_NUM = GPU_NUM = renom.cuda.cuGetDeviceCount()
    except Exception:
        pass

def _create_dirs():
    # Create directories
    for path in [DATASRC_PREDICTION, DB_DIR_TRAINED_WEIGHT]:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Directory %s is newly created." % (path))

def main():
    _init_cuda()
    _create_dirs()
    db.initdb(DB_DIR)

    # Parser settings.
    parser = argparse.ArgumentParser(description='ReNomRG')
    parser.add_argument('--host', default='0.0.0.0', help='Server address')
    parser.add_argument('--port', default='8080', help='Server port')

    args = parser.parse_args()
    wsgiapp = default_app()
    httpd = wsgi_server.Server(wsgiapp, host=args.host, port=int(args.port))
    httpd.serve_forever()


if __name__ == "__main__":
    main()
