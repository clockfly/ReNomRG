# coding: utf-8

import threading
import logging
import argparse
import os
import json
import pkg_resources
import mimetypes
import posixpath
import traceback
import pandas as pd
import numpy as np
import pickle

from bottle import HTTPResponse, default_app, route, request, error, abort, static_file
from concurrent.futures import ThreadPoolExecutor as Executor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import CancelledError
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

import renom as rm
import renom.cuda
from renom.cuda import set_cuda_active, release_mem_pool, use_device

from renom_rg.server import DATASRC_DIR, DB_DIR_TRAINED_WEIGHT
from renom_rg.server import wsgi_server
from . import *
from . import db
from . import train_task
from . import pred_task

logger = logging.getLogger(__name__)

gpupool = None

def create_response(body, status=200, err=None):
    body['err'] = err
    r = HTTPResponse(status=status, body=body)
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
    path = posixpath.join('.build', path, filename)
    try:
        body = pkg_resources.resource_string(__name__, path)
    except FileNotFoundError:
        return HTTPResponse(status=404)

    headers = {}
    mimetype, encoding = mimetypes.guess_type(filename)
    if mimetype:
        headers['Content-Type'] = mimetype
    if encoding:
        headers['encoding'] = encoding
    return HTTPResponse(body, **headers)


def split_target(data, ids):
    indexes = np.ones(data.shape[1], dtype=bool)
    indexes[ids] = False
    X = data.loc[:, indexes]
    y = data.loc[:, ~indexes]
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


@route('/api/renom_rg/datasets/labels', method='GET')
def get_labels():
    with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
        data = pickle.load(f)
    body = {"labels": list(data.columns)}
    r = create_response(body)
    return r

def _dataset_to_dict(ds):
    ret = {
        "dataset_id": ds.id,
        "name": ds.name,
        "description": ds.description,
        "target_column_ids": pickle.loads(ds.target_column_ids),
        "labels": pickle.loads(ds.labels),
        "train_ratio": ds.train_ratio,
        "train_index": pickle.loads(ds.train_index),
        "valid_index": pickle.loads(ds.valid_index),
        "target_train": pickle.loads(ds.target_train),
        "target_valid": pickle.loads(ds.target_valid),
        "created": ds.created.isoformat()
    }
    return ret


@route('/api/renom_rg/datasets', method='GET')
def get_datasets():
    q = db.session().query(db.DatasetDef).all()
    ret = [_dataset_to_dict(ds) for ds in q]
    return create_response({'datasets': ret})


@route('/api/renom_rg/datasets/<dataset_id:int>', method='GET')
def get_dataset(dataset_id):
    ds = db.session().query(db.DatasetDef).get(dataset_id)
    if ds:
        return create_response({'dataset': _dataset_to_dict(ds)})
    else:
        return create_response({}, 404, err='not found')


@route('/api/renom_rg/datasets/confirm', method='POST')
def confirm_dataset():
    target_column_ids = json.loads(request.params.target_column_ids)
    train_ratio = float(request.params.train_ratio)

    with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
        data = pickle.load(f)
    print(data.shape)
    X, y = split_target(data, target_column_ids)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=(1 - train_ratio))

    body = {
        "train_count": y_train.shape[0],
        "valid_count": y_valid.shape[0],
        "target_train": y_train.T.values.tolist(),
        "target_valid": y_valid.T.values.tolist(),
        "train_index": np.array(y_train.index).tolist(),
        "valid_index": np.array(y_valid.index).tolist()
    }
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets', method='POST')
def create_dataset():
    name = request.params.name
    description = request.params.description
    target_column_ids = json.loads(request.params.target_column_ids)
    labels = json.loads(request.params.labels)
    train_ratio = float(request.params.train_ratio)
    train_index = json.loads(request.params.train_index)
    valid_index = json.loads(request.params.valid_index)
    target_train = json.loads(request.params.target_train)
    target_valid = json.loads(request.params.target_valid)

    dataset = db.DatasetDef(name=name, description=description,
                            target_column_ids=pickle.dumps(target_column_ids),
                            labels=pickle.dumps(labels),
                            train_ratio=train_ratio,
                            train_index=pickle.dumps(train_index),
                            valid_index=pickle.dumps(valid_index),
                            target_train=pickle.dumps(target_train),
                            target_valid=pickle.dumps(target_valid))
    session = db.session()
    session.add(dataset)
    session.commit()

    return create_response({'dataset': _dataset_to_dict(dataset)})


@route('/api/renom_rg/datasets/<dataset_id:int>', method='DELETE')
def delete_dataset(dataset_id):
    session = db.session()
    ds = session.query(db.DatasetDef).get(dataset_id)

    if ds:
        session.delete(ds)
        return create_response({})
    else:
        return create_response({}, 404, err='dataset not found')


def _model_to_dict(model):
    ret = {
        'model_id': model.id,
        'dataset_id': model.dataset_id,
        'state': model.state,
        'algorithm': model.algorithm,
        'algorithm_params': pickle.loads(model.algorithm_params),
        'batch_size': model.batch_size,
        'epoch': model.epoch,
        'train_loss_list': pickle.loads(model.train_loss_list),
        'valid_loss_list': pickle.loads(model.valid_loss_list),
        'best_epoch': model.best_epoch,
        'best_epoch_valid_loss': model.best_epoch_valid_loss,
        'best_epoch_rmse': model.best_epoch_rmse,
        'best_epoch_max_abs_error': model.best_epoch_max_abs_error,
        'best_epoch_r2': model.best_epoch_r2,
        'valid_predicted': pickle.loads(model.valid_predicted),
        'valid_true': pickle.loads(model.valid_true),
        'sampled_train_pred': pickle.loads(model.sampled_train_pred),
        'sampled_train_true': pickle.loads(model.sampled_train_true),
        'confidence_data': pickle.loads(model.confidence_data),
        'weight': model.weight,
        'deployed': model.deployed,
        'created': model.created.isoformat(),
        'updated': model.updated.isoformat(),
    }
    return ret

@route("/api/renom_rg/models", method="GET")
def get_models():
    q = db.session().query(db.Model).order_by(db.Model.id.desc()).all()
    ret = [_model_to_dict(model) for model in q]
    return create_response({'models': ret})


@route("/api/renom_rg/models/<model_id:int>", method="GET")
def get_model(model_id):
    model = db.session().query(db.Model).get(model_id)
    if model:
        return create_response(_model_to_dict(model))
    else:
        return create_response({}, 404, err='not found')


@route("/api/renom_rg/models", method="POST")
def create_model():
    dataset_id = int(request.params.dataset_id)
    algorithm = int(request.params.algorithm)
    algorithm_params = json.loads(request.params.algorithm_params)
    batch_size = int(request.params.batch_size)
    epoch = int(request.params.epoch)

    model = db.Model(dataset_id=dataset_id, algorithm=algorithm,
                     algorithm_params=pickle.dumps(algorithm_params), batch_size=batch_size,
                     epoch=epoch)

    session = db.session()
    session.add(model)
    session.commit()

    return create_response(_model_to_dict(model))


def _taskstate_to_dict(th):
    ret = {
        "model_id": th.model_id,
        "algorithm": th.taskstate.algorithm,
        "nth_epoch": th.taskstate.nth_epoch,
        "nth_batch": th.taskstate.nth_batch,
        "train_loss": th.taskstate.train_loss,
        "total_epoch": th.taskstate.total_epoch,
        "total_batch": th.taskstate.total_batch
    }
    return ret


@route("/api/renom_rg/models/running", method="GET")
def get_running_models():
    ret = [_taskstate_to_dict(th) for th in train_thread_pool.values()]
    return create_response({'running_models': ret})


@route("/api/renom_rg/models/<model_id:int>", method="DELETE")
def delete_model(model_id):
    q = db.session().query(db.Model).filter(db.Model.id == model_id)
    n = q.delete()
    if n:
        return create_response({})
    else:
        return create_response({}, 404, err='model not found')


@route("/api/renom_rg/models/<model_id:int>/deploy", method="POST")
def deploy_model(model_id):
    session = db.session()

    session.query(db.Model).update({'deployed': 0})
    model = session.query(db.Model).get(model_id)

    if model:
        model.deployed = 1
        session.add(model)
        session.commit()

        return create_response({'model': _model_to_dict(model)})
    else:
        return create_response({}, 404, err='not found')


@route("/api/renom_rg/models/<model_id:int>/undeploy", method="POST")
def undeploy_model(model_id):
    session = db.session()

    model = session.query(db.Model).get(model_id)
    if model:
        model.deployed = 0
        session.add(model)
        session.commit()

        return create_response({'model': _model_to_dict(model)})
    else:
        return create_response({}, 404, err='not found')


def submit_task(executor, f, *args, **kwargs):
    if gpupool:
        return executor.submit(gpupool.run, f, *args, **kwargs)
    else:
        return executor.submit(f, *args, **kwargs)


executor = Executor()

@route("/api/renom_rg/models/<model_id:int>/train", method="GET")
def train_model(model_id):
    model = db.session().query(db.Model).get(model_id)
    if not model:
        return create_response({}, 404, err='model not found')

    th = train_task.TrainThread()
    taskstate = train_task.TaskState.add_task(model)
    train_thread_pool[model.id] = th
    f = submit_task(executor, th.train, taskstate, model.id)
    try:
        f.result()
        return create_response({'result': 'ok'})

    except Exception as e:
        traceback.print_exc()
        return create_response({"error_msg": str(e)})

    finally:
        del train_thread_pool[model.id]
        if renom.cuda.has_cuda():
            release_mem_pool()



@route("/api/renom_rg/models/<model_id:int>/predict", method="GET")
def predict_model(model_id):
    model = db.session().query(db.Model).get(model_id)
    if not model:
        return create_response({}, 404, err='model not found')

    try:
        with open(os.path.join(DATASRC_DIR, 'prediction_set', 'pred.pickle'), mode='rb') as f:
            data = np.array(pickle.load(f))
    except Exception as e:
        traceback.print_exc()
        return create_response({}, 404, err=str(e))

    f = submit_task(executor, pred_task.prediction, model.id, data)
    try:
        result = f.result()
        body = {
            'pred_x': data.tolist(),
            'pred_y': result.tolist()
        }
        return create_response(body)

    except Exception as e:
        traceback.print_exc()
        return create_response({}, 404, err=str(e))

    finally:
        if renom.cuda.has_cuda():
            release_mem_pool()


@route("/api/renom_rg/deployed_model/pull", method="GET")
def pull_deployed_model():
    model = db.session().query(db.Model).filter(db.Model.deployed == 1).one()
    if model:
        file_name = model.weight
        return static_file(file_name, root=DB_DIR_TRAINED_WEIGHT, download='deployed_model.h5')
    else:
        return create_response({}, 404, err='model not found')


@route("/api/renom_rg/deployed_model", method="GET")
def get_deployed_model():
    model = db.session().query(db.Model).filter(db.Model.deployed == 1).one()
    if model:
        return create_response(_model_to_dict(model))
    else:
        return create_response({}, 404, err='not found')


def _create_dirs():
    # Create directories
    for path in [DATASRC_PREDICTION, DB_DIR_TRAINED_WEIGHT]:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Directory %s is newly created." % (path))


def plugin(func):
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            db.session().commit()
            return ret

        except Exception as e:
            logger.exception("Exception:")
            db.session().rollback()
            return (500, str(e))

    return wrapper


def get_app():
    app = default_app()
    app.install(plugin)
    return app


class GPUPool:
    active_gpu = threading.local()

    def __init__(self, num):
        self.gpu_resource = threading.Semaphore(num)
        self.gpus = set(range(num))

    def run(self, f, *args, **kwargs):
        with self.gpu_resource:
            self.active_gpu.id = self.gpus.pop()
            try:
                set_cuda_active(True)
                with use_device(self.active_gpu.id):
                    return f(*args, **kwargs)
            finally:
                self.gpus.add(self.active_gpu.id)
                release_mem_pool()


def _init_gpu():
    global gpupool
    if renom.cuda.has_cuda():
        num = renom.cuda.cuGetDeviceCount()
        gpupool = GPUPool(num)


def _init_train_thread_pool():
    global train_thread_pool
    train_thread_pool = {}


def main():
    _create_dirs()
    db.initdb()
    _init_gpu()
    _init_train_thread_pool()

    # Parser settings.
    parser = argparse.ArgumentParser(description='ReNomRG')
    parser.add_argument('--host', default='0.0.0.0', help='Server address')
    parser.add_argument('--port', default='8080', help='Server port')

    args = parser.parse_args()
    wsgiapp = get_app()
    httpd = wsgi_server.Server(wsgiapp, host=args.host, port=int(args.port))
    httpd.serve_forever()


if __name__ == "__main__":
    main()
