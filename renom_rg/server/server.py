# coding: utf-8

import threading
import logging
import argparse
import os
import sys
import json
import pkg_resources
import mimetypes
import posixpath
import traceback
import pandas as pd
import numpy as np
import pickle
import uuid
import shutil
import csv
import datetime

from bottle import HTTPResponse, default_app, route, request, error, abort, static_file
from concurrent.futures import ThreadPoolExecutor as Executor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import CancelledError
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sqlalchemy.sql import exists

from renom_rg.server import DATASRC_PREDICTION_OUT, SCRIPT_DIR

import renom as rm
import renom.cuda
from renom.cuda import set_cuda_active, release_mem_pool, use_device

import renom_rg.db
from renom_rg.server import DATASRC_DIR, DB_DIR_TRAINED_WEIGHT, DB_DIR_ML_MODELS
from renom_rg.server import wsgi_server
from . import *
from . import db
from . import train_task
from . import pred_task

logger = logging.getLogger(__name__)

gpupool = None


def create_response(body, status=200, err=None):
    body['err'] = err
#    body = json.dumps(body, allow_nan=False)
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


def split_target(data, labels, ids):
    del_labels = []
    for index, item in enumerate(labels):
        if index not in ids:
            if item in data.columns.values:
                del_labels.append(item)
        else:
            if item not in data.columns.values:
                raise ValueError('Explanatory variable "%s" of Dataset is not '\
                                 'included in prediction data "pred.pickle"' % item)

    split_data = data.drop(columns=del_labels)
    return split_data


def scaling(pd_yx, selected_scaling, name, type):
    if selected_scaling == 2:
        scaler = preprocessing.StandardScaler()
        ss = 'standardization'
    elif selected_scaling == 3:
        scaler = preprocessing.MinMaxScaler()
        ss = 'normalization'
    np_result = scaler.fit_transform(pd_yx)
    result = pd.DataFrame(np_result)

    SCALING_DIR = os.path.join(DATASRC_PREDICTION_OUT, 'dataset_scaling')
    if not os.path.isdir(SCALING_DIR):
        os.makedirs(SCALING_DIR)
    now = datetime.datetime.now()
    filename = 'scaler_' + name + '_' + type + '_' + ss + '_{0:%Y%m%d%H%M%S}.pickle'.format(now)
    filepath = os.path.join(SCALING_DIR, filename)
    with open(filepath, mode='wb') as f:
        pickle.dump(scaler, f)
    return result, filename


def scaling_again(np_x, filename_X):
    SCALING_DIR = os.path.join(DATASRC_PREDICTION_OUT, 'dataset_scaling')
    filepath = os.path.join(SCALING_DIR, filename_X)
    with open(filepath, mode='rb') as f:
        scaler = pickle.load(f)
    result = scaler.transform(np_x)
    return result


def re_scaling(np_y, filename_y):
    SCALING_DIR = os.path.join(DATASRC_PREDICTION_OUT, 'dataset_scaling')
    filepath = os.path.join(SCALING_DIR, filename_y)
    with open(filepath, mode='rb') as f:
        scaler = pickle.load(f)
    result = scaler.inverse_transform(np_y)
    return result


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
        "explanatory_column_ids": pickle.loads(ds.explanatory_column_ids),
        "target_column_ids": pickle.loads(ds.target_column_ids),
        "labels": pickle.loads(ds.labels),
        "train_ratio": ds.train_ratio,
        "train_index": pickle.loads(ds.train_index),
        "valid_index": pickle.loads(ds.valid_index),
        "true_histogram": pickle.loads(ds.true_histogram),
        "selected_scaling": ds.selected_scaling,
        "filename_y": ds.filename_y,
        "filename_X": ds.filename_X,
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
    name = request.params.name
    labels = json.loads(request.params.labels)
    explanatory_column_ids = json.loads(request.params.explanatory_column_ids)
    target_column_ids = json.loads(request.params.target_column_ids)
    train_ratio = float(request.params.train_ratio)
    selected_scaling = int(request.params.selected_scaling)

    with open(os.path.join(DATASRC_DIR, 'data.pickle'), mode='rb') as f:
        data = pickle.load(f)
    X = split_target(data, labels, explanatory_column_ids)
    y = split_target(data, labels, target_column_ids)

    filename_y = 'none_scaling'
    filename_X = 'none_scaling'
    if selected_scaling != 1:
        y, filename_y = scaling(y, selected_scaling, name, type='y')
        X, filename_X = scaling(X, selected_scaling, name, type='X')

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=(1 - train_ratio))

    num_bin = 10
    # true histogram
    true_histogram = []
    for i in range(y_valid.shape[1]):
        counts, bins = np.histogram(y_train.iloc[:, i], bins=num_bin)
        train_true_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
        counts, bins = np.histogram(y_valid.iloc[:, i], bins=num_bin)
        valid_true_histogram = {"counts": counts.tolist(), "bins": bins.tolist()}
        true_histogram.append({"train": train_true_histogram, "valid": valid_true_histogram})

    body = {
        "train_count": y_train.shape[0],
        "valid_count": y_valid.shape[0],
        "train_index": np.array(y_train.index).tolist(),
        "valid_index": np.array(y_valid.index).tolist(),
        "true_histogram": true_histogram,
        "filename_y": filename_y,
        "filename_X": filename_X
    }
    r = create_response(body)
    return r


@route('/api/renom_rg/datasets', method='POST')
def create_dataset():
    name = request.params.name
    description = request.params.description
    explanatory_column_ids = json.loads(request.params.explanatory_column_ids)
    target_column_ids = json.loads(request.params.target_column_ids)
    selected_scaling = int(request.params.selected_scaling)
    labels = json.loads(request.params.labels)
    train_ratio = float(request.params.train_ratio)
    train_index = json.loads(request.params.train_index)
    valid_index = json.loads(request.params.valid_index)
    true_histogram = json.loads(request.params.true_histogram)
    filename_y = request.params.filename_y
    filename_X = request.params.filename_X

    dataset = db.DatasetDef(name=name, description=description,
                            explanatory_column_ids=pickle.dumps(explanatory_column_ids),
                            target_column_ids=pickle.dumps(target_column_ids),
                            labels=pickle.dumps(labels),
                            train_ratio=train_ratio,
                            train_index=pickle.dumps(train_index),
                            valid_index=pickle.dumps(valid_index),
                            true_histogram=pickle.dumps(true_histogram),
                            selected_scaling=selected_scaling,
                            filename_y=filename_y,
                            filename_X=filename_X)
    session = db.session()
    session.add(dataset)
    session.commit()

    return create_response({'dataset': _dataset_to_dict(dataset)})


@route('/api/renom_rg/datasets/<dataset_id:int>', method='DELETE')
def delete_dataset(dataset_id):
    session = db.session()

    ds = session.query(db.DatasetDef).get(dataset_id)

    if ds:
        q = session.query(db.Model.id).filter(db.Model.dataset_id == dataset_id)
        (session.query(db.ParamSearcherModel)
         .filter(db.ParamSearcherModel.model_id.in_(q))
         .delete(synchronize_session=False))

        session.query(db.Model).filter(db.Model.dataset_id == dataset_id).delete()
        session.delete(ds)
        session.commit()
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
        'true_histogram': pickle.loads(model.true_histogram),
        'pred_histogram': pickle.loads(model.pred_histogram),
        'confidence_data': pickle.loads(model.confidence_data),
        'weight': model.weight,
        'model_pickle': model.model_pickle,
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
    session = db.session()

    searcher = None
    searcher_id = request.params.get('searcher_id', None)
    if searcher_id is not None:
        searcher = (session.query(db.ParamSearcher)
                    .filter_by(id=int(searcher_id)).one())

    dataset_id = int(request.params.dataset_id)
    algorithm = int(request.params.algorithm)
    algorithm_params = json.loads(request.params.algorithm_params)
    batch_size = int(request.params.batch_size)
    epoch = int(request.params.epoch)

    try:
        # if user input file is not exists
        if algorithm_params['script_file_name'] is not '':
            script = algorithm_params['script_file_name']
            scriptdir = os.path.abspath(SCRIPT_DIR)
            if not scriptdir.endswith(os.path.sep):
                scriptdir += os.path.sep

            scriptfile = os.path.abspath(os.path.join(scriptdir, script))
            if not scriptfile.startswith(scriptdir):
                raise ValueError('Invalid script name: %s' % scriptfile)
            elif not os.path.exists(scriptfile):
                raise ValueError('Invalid script name: %s' % scriptfile)

        print(algorithm_params['script_file_name'])

        model = db.Model(dataset_id=dataset_id, algorithm=algorithm,
                         algorithm_params=pickle.dumps(algorithm_params), batch_size=batch_size,
                         epoch=epoch)

        session.add(model)
        session.commit()

        if searcher:
            searchermodel = db.ParamSearcherModel(searcher=searcher, model=model)
            session.add(searchermodel)
            session.commit()

        return create_response(_model_to_dict(model))
    except Exception as e:
        traceback.print_exc()
        return create_response({}, 500, err=str(e))


def _taskstate_to_dict(taskstate):
    ret = {
        "model_id": taskstate.model_id,
        "algorithm": taskstate.algorithm,
        "nth_epoch": taskstate.nth_epoch,
        "nth_batch": taskstate.nth_batch,
        "train_loss": taskstate.train_loss,
        "total_epoch": taskstate.total_epoch,
        "total_batch": taskstate.total_batch
    }
    return ret


@route("/api/renom_rg/models/running", method="GET")
def get_running_models():
    ret = [_taskstate_to_dict(taskstate) for taskstate in train_task.TaskState.tasks.values()]
    return create_response({'running_models': ret})


MODEL_WAIT_TIMEOUT = 60

SERVER_ID = uuid.uuid4().hex

@route("/api/renom_rg/models/wait_model_update", method="GET")
def wait_model_update():
    server_id = request.get_cookie("server_id")
    cur_serial = None
    if server_id == SERVER_ID:
        serial_cookie = request.get_cookie("model_serial")
        cur_serial = int(serial_cookie) if serial_cookie else None

    ev = train_task.TaskState.add_event(cur_serial)

    updated = ev.wait(MODEL_WAIT_TIMEOUT)
    resp = create_response({'updated': updated})

    new_serial = train_task.TaskState.serial
    resp.set_cookie("model_serial", str(new_serial))
    resp.set_cookie("server_id", SERVER_ID)

    return resp


@route("/api/renom_rg/models/<model_id:int>", method="DELETE")
def delete_model(model_id):
    session = db.session()
    session.query(db.ParamSearcherModel).filter_by(model_id=model_id).delete()
    q = session.query(db.Model).filter_by(id=model_id)
    n = q.delete()
    if n:
        session.commit()
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

    taskstate = train_task.TaskState.add_task(model)
    f = submit_task(executor, train_task.train, taskstate, model.id)
    try:
        f.result()
        return create_response({'result': 'ok'})

    except Exception as e:
        traceback.print_exc()
        return create_response({}, 500, err=str(e))

    finally:
        if renom.cuda.has_cuda():
            release_mem_pool()


@route("/api/renom_rg/models/<model_id:int>/stop", method="GET")
def stop_model(model_id):
    try:
        train_task.TaskState.tasks[model_id].canceled = True
    except Exception as e:
        traceback.print_exc()
        return create_response({"error_msg": str(e)})


@route("/api/renom_rg/models/<model_id:int>/predict", method="POST")
def predict_model(model_id):
    explanatory_column = request.params.explanatory_column
    target_column = request.params.target_column
    explanatory_column_ids = json.loads(request.params.explanatory_column_ids)

    model = db.session().query(db.Model).get(model_id)
    if not model:
        return create_response({}, 404, err='model not found')

    try:
        with open(os.path.join(DATASRC_DIR, 'prediction_set', 'pred.pickle'), mode='rb') as f:
            p_all_data = pickle.load(f)
        p_X = split_target(p_all_data, pickle.loads(model.dataset.labels), explanatory_column_ids)
        n_X = np.array(p_X)
        selected_scaling = model.dataset.selected_scaling
        if selected_scaling != 1:
            filename_X = model.dataset.filename_X
            n_X_scaling = scaling_again(n_X, filename_X)
        else:
            n_X_scaling = n_X
    except Exception as e:
        traceback.print_exc()
        return create_response({}, 404, err=str(e))

    f = submit_task(executor, pred_task.prediction, model.id, n_X_scaling)
    try:
        result = f.result()
        if selected_scaling != 1:
            filename_y = model.dataset.filename_y
            result = re_scaling(result, filename_y)

        CSV_DIR = os.path.join(DATASRC_PREDICTION_OUT, 'csv')
        if not os.path.isdir(CSV_DIR):
            os.makedirs(CSV_DIR)
        now = datetime.datetime.now()
        filename = 'model' + str(model_id) + '_{0:%Y%m%d%H%M%S}'.format(now) + '.csv'
        filepath = os.path.join(CSV_DIR, filename)

        target_labels = target_column.split(',')
        explanatory_labels = explanatory_column.split(',')
        labels = target_labels + explanatory_labels
        np_xy = np.round(np.c_[result, n_X], 3)
        pred_x_y = pd.DataFrame(np_xy)
        pred_x_y.columns = labels
        pred_x_y.to_csv(filepath, index=False)

        body = {
            'pred_x': n_X.tolist(),
            'pred_y': result.tolist(),
            'pred_csv': filename
        }

        return create_response(body)

    except Exception as e:
        traceback.print_exc()
        return create_response({}, 404, err=str(e))

    finally:
        if renom.cuda.has_cuda():
            release_mem_pool()


@route("/api/renom_rg/models/predict/csv/<filename>", method="GET")
def predict_csv(filename):
    CSV_DIR = os.path.join(DATASRC_PREDICTION_OUT, 'csv')
    try:
        return static_file(filename, root=CSV_DIR, download=True)
    except Exception as e:
        traceback.print_exc()
        body = json.dumps({"error_msg": e.args[0]})
        ret = create_response(body)
        return ret


@route("/api/renom_rg/deployed_model", method="GET")
def get_deployed_model_weight():
    model = db.session().query(db.Model).filter(db.Model.deployed == 1).one()
    if model:
        if model.weight:
            file_name = model.weight
            return static_file(file_name, root=DB_DIR_TRAINED_WEIGHT, download='deployed_model.h5')
        elif model.model_pickle:
            m_file_name = model.model_pickle
            return static_file(m_file_name, root=DB_DIR_ML_MODELS, download='deployed_model.pickle')
    else:
        return create_response({}, 404, err='model not found')


@route("/api/renom_rg/deployed_model_info", method="GET")
def get_deployed_model_info():
    model = db.session().query(db.Model).filter(db.Model.deployed == 1).one()
    if model:
        model_dict = _model_to_dict(model)
        model_dict["explanatory_column_ids"] = pickle.loads(model.dataset.explanatory_column_ids)
        return create_response(model_dict)
    else:
        return create_response({}, 404, err='not found')


@route("/api/renom_rg/searchers", method="POST")
def create_searcher():
    info = json.loads(request.params.info)

    searcher = db.ParamSearcher(info=pickle.dumps(info))

    session = db.session()
    session.add(searcher)
    session.commit()

    return create_response({'id': searcher.id})


@route("/api/renom_rg/searchers/<searcher_id:int>", method="DELETE")
def delete_searcher(searcher_id):
    session = db.session()
    session.query(db.ParamSearcherModel).filter_by(searcher_id=searcher_id).delete()
    n = session.query(db.ParamSearcher).filter_by(id=searcher_id).delete()
    if n:
        session.commit()
        return create_response({})
    else:
        return create_response({}, 404, err='searcher not found')


def searcher_to_dict(searcher):
    modelids = [m.model_id for m in searcher.searcher_models]
    taskstate = []
    for modelid in modelids:
        if modelid in train_task.TaskState.tasks:
            taskstate.append(_taskstate_to_dict(train_task.TaskState.tasks[modelid]))

    return {
        'id': searcher.id,
        'info': pickle.loads(searcher.info),
        'model_ids': modelids,
        'taskstates': taskstate,
    }


@route("/api/renom_rg/searchers", method="GET")
def get_searchers():
    session = db.session()

    searchers = session.query(db.ParamSearcher)
    dicts = [searcher_to_dict(searcher) for searcher in searchers]
    return create_response({
        'searchers': dicts
    })


@route("/api/renom_rg/searchers/<searcher_id:int>", method="GET")
def get_searcher(searcher_id):
    session = db.session()
    searcher = session.query(db.ParamSearcher).get(searcher_id)
    if searcher:
        return create_response(searcher_to_dict(searcher))
    else:
        return create_response({}, 404, err='not found')


def _create_dirs():
    # Create directories
    for path in [SCRIPT_DIR, DATASRC_PREDICTION, DB_DIR_TRAINED_WEIGHT]:

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


def _cp_alembic():
    rgdbpath = list(renom_rg.db.__path__)[0]
    # copy alembic.ini
    inifile = os.path.join(rgdbpath, "alembic.ini")
    outfile = os.path.join(os.getcwd(), "alembic.ini")
    if not os.path.exists(outfile):
        shutil.copy(inifile, outfile)

    # copy alembic dir
    alembicdir = os.path.join(rgdbpath, "alembic")
    outdir = os.path.join(os.getcwd(), "alembic")
    if not os.path.isdir(outdir):
        shutil.copytree(alembicdir, outdir)


def main():
    _cp_alembic()
    _create_dirs()
    db.initdb()
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
