# coding: utf-8

import threading
import weakref
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
try:
    import cPickle as pickle
except:
    import pickle


from bottle import HTTPResponse, default_app, route, request, error, abort
from concurrent.futures import ThreadPoolExecutor as Executor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import CancelledError
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

import renom as rm
import renom.cuda
from renom.cuda import set_cuda_active, release_mem_pool, use_device

from renom_rg.server import MAX_THREAD_NUM, DATASRC_DIR, STATE_RESERVED, STATE_RUNNING, STATE_FINISHED, STATE_DELETED
from renom_rg.server import wsgi_server
from . import *
from . import db
from . import train_task

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


def create_error_body(e):
    return {"error_msg": str(e)}


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
        "target_column_id": ds.target_column_id,
        "labels": pickle.loads(ds.labels),
        "train_ratio": ds.train_ratio,
        "train_index": pickle.loads(ds.train_index),
        "valid_index": pickle.loads(ds.valid_index),
        "created": ds.created.isoformat()
    }
    return ret


@route('/api/renom_rg/datasets', method='GET')
def get_datasets():
    q = db.session.query(db.DatasetDef).all()
    ret = [_dataset_to_dict(ds) for ds in q]
    return create_response({'datasets':ret})


@route('/api/renom_rg/datasets/<dataset_id:int>', method='GET')
def get_dataset(dataset_id):
    ds = db.session.query(db.DatasetDef).get(dataset_id)
    if ds:
        return create_response({'dataset':_dataset_to_dict(ds)})
    else:
        return create_response({}, 404, err='not found')


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
    name = request.params.name
    description = request.params.description
    target_column_id = int(request.params.target_column_id)
    labels = json.loads(request.params.labels)
    train_ratio = float(request.params.train_ratio)
    train_index = json.loads(request.params.train_index)
    valid_index = json.loads(request.params.valid_index)

    dataset = db.DatasetDef(name=name, description=description,
                            target_column_id=target_column_id,
                            labels=pickle.dumps(labels),
                            train_ratio=train_ratio,
                            train_index=pickle.dumps(train_index),
                            valid_index=pickle.dumps(valid_index))

    db.session.add(dataset)
    db.session.commit()

    return create_response({'dataset':_dataset_to_dict(dataset)})


@route('/api/renom_rg/datasets/<dataset_id:int>', method='DELETE')
def delete_dataset(dataset_id):
    ds = db.session.query(db.DatasetDef).get(dataset_id)

    if ds:
        db.session.delete(ds)
        return create_response({})
    else:
        return create_response({}, 404, err='dataset not found')


def _model_to_dict(model):
    ret = {
        'id': model.id,
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
        'weight': model.weight,
        'deployed': model.deployed,
        'created': model.created.isoformat(),
        'updated': model.updated.isoformat(),
    }
    return ret

@route("/api/renom_rg/models", method="GET")
def get_models():
    q = db.session.query(db.Model).all()
    ret = [_model_to_dict(model) for model in q]
    return create_response({'models':ret})


@route("/api/renom_rg/models/<model_id:int>", method="GET")
def get_model(model_id):
    model = db.session.query(db.Model).get(model_id)
    if model:
        return create_response({'model':_model_to_dict(model)})
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
    db.session.add(model)
    db.session.commit()

    return create_response({'model':_model_to_dict(model)})


@route("/api/renom_rg/models/<model_id:int>", method="DELETE")
def delete_model(model_id):
    q = db.session.query(db.Model).filter(db.Model.id==model_id)
    n = q.delete() 
    if n:
        return create_response({})
    else:
        return create_response({}, 404, err='model not found')


@route("/api/renom_rg/models/<model_id:int>/deploy", method="POST")
def deploy_model(model_id):
    db.session.query(db.Model).update({'deployed': 0})
    model = db.session.query(db.Model).get(model_id)

    if model:
        model.deployed = 1
        db.session.add(model)
        db.session.commit()

        return create_response({'model':_model_to_dict(model)})
    else:
        return create_response({}, 404, err='not found')


@route("/api/renom_rg/models/<model_id:int>/undeploy", method="POST")
def undeploy_model(model_id):
    db.session.query(db.Model).update({'deployed': 0})
    model = db.session.query(db.Model).get(model_id)

    if model:
        model.deployed = 1
        db.session.add(model)
        db.session.commit()

        return create_response({'model':_model_to_dict(model)})
    else:
        return create_response({}, 404, err='not found')


def submit_task(executor, f, *args, **kwargs):
    if gpupool:
        return executor.submit(gpupool.run, f, *args, **kwargs)
    else:
        return executor.submit(f, *args, **kwargs)


class TaskStatus:
    tasks = weakref.WeakValueDictionary()  # Mapping of {model.id: TaskStatus()}

    @classmethod
    def add_task(cls, model):
        ret = TaskStatus()
        cls.tasks[model.id] = ret
        return ret

    canceled = False

executor = Executor()

@route("/api/renom_rg/models/<model_id:int>/train", method="GET")
def train_model(model_id):
    model = db.session.query(db.Model).get(model_id)
    if not model:
        return create_response({}, 404, err='not found')

    taskstatus = TaskStatus.add_task(model)
    f = submit_task(executor, train_task.train, taskstatus, model)
    try:
        ret = f.result()
        return create_response(ret)

    except Exception as e:
        return create_response({"error_msg": e.error_msg})

    finally:
        if renom.cuda.has_cuda():
            release_mem_pool()



@route("/api/renom_rg/models/<model_id:int>/predict", method="GET")
def predict_model(model_id):
    try:
        # run prediction thread
        body = {}
    except Exception as e:
        body = create_error_body(e)
    r = create_response(body)
    return r


def _create_dirs():
    # Create directories
    for path in [DATASRC_PREDICTION, DB_DIR_TRAINED_WEIGHT]:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Directory %s is newly created." % (path))


def plugin(func):
    def wrapper(*args,**kwargs):
        try:
            ret = func(*args,**kwargs)
            db.session.commit()
            return ret

        except Exception as e:
            logger.exception("Exception:")
            db.session.rollback()
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


def main():
    _create_dirs()
    _init_gpu()

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
