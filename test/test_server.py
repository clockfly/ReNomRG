import os
import time
import pickle
import random
import json
import pytest
import threading
from renom_rg.server import db, server, train_task
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor


def test_index(app):
    resp = app.get('/')
    assert resp.status_int == 200
    assert resp.headers['content-type'] == 'text/html'
    assert resp.text.strip()


def test_static(app):
    resp = app.get('/static/css/init.css')
    assert resp.status_int == 200
    assert resp.headers['content-type'] == 'text/css'
    assert resp.text.strip()


def test_css(app):
    resp = app.get('/css/init.css')
    assert resp.status_int == 200
    assert resp.headers['content-type'] == 'text/css'
    assert resp.text.strip()


def test_404(app):
    resp = app.get('/css/none', expect_errors=True)
    assert resp.status_int == 404



def test_get_labels(app, data_pickle):
    resp = app.get('/api/renom_rg/datasets/labels')

    assert resp.status_int == 200
    assert resp.json['labels']


def test_create_dataset(app):
    resp = app.post('/api/renom_rg/datasets', {
        'name': 'test_create_dataset_1',
        'description': 'description',
        'target_column_ids': json.dumps([1, 2]),
        'selected_scaling': 2,
        'labels': json.dumps([1, 2, 3, 4]),
        'train_ratio': 0.1,
        'train_index': json.dumps([5, 6]),
        'valid_index': json.dumps([7, 8]),
        'target_train': json.dumps([1, 2]),
        'target_valid': json.dumps([1, 2]),
        'true_histogram': json.dumps([{'train': {'counts': [1, 2],
                                                 'bins': [1, 2]},
                                       'valid': {'counts': [1, 2],
                                                 'bins': [1, 2]}}])
    })

    assert resp.status_int == 200
    q = db.session().query(db.DatasetDef)
    ds = q.filter(db.DatasetDef.name == 'test_create_dataset_1').one()
    assert ds
    assert resp.json['dataset']['dataset_id'] == ds.id


def _add_dataset():
    name = str(random.random())
    ds = db.DatasetDef(name=name, description='description',
                       target_column_ids=pickle.dumps([0]),
                       labels=pickle.dumps([1, 2, 3]),
                       train_ratio=0.1,
                       train_index=pickle.dumps(list(range(1, 405))),
                       valid_index=pickle.dumps(list(range(405, 500))),
                       target_train=pickle.dumps([1, 2]),
                       target_valid=pickle.dumps([1, 2]),
                       true_histogram=pickle.dumps([{'train': {'counts': [1, 2],
                                                               'bins': [1, 2]},
                                                     'valid': {'counts': [1, 2],
                                                               'bins': [1, 2]}}]))

    session = db.session()
    session.add(ds)
    session.commit()
    return ds


def test_delete_dataset(app):
    ds = _add_dataset()
    searcher = _add_searcher()
    model = _add_model(dataset=ds, searcher=searcher)

    resp = app.delete('/api/renom_rg/datasets/%d' % ds.id)

    assert resp.status_int == 200
    assert db.session().query(db.DatasetDef).filter(db.DatasetDef.id == ds.id).count() == 0

    resp = app.delete('/api/renom_rg/datasets/%d' % ds.id)
    assert resp.status_int == 404


def test_get_dataset(app):
    ds = _add_dataset()
    resp = app.get('/api/renom_rg/datasets/%d' % ds.id)

    assert resp.status_int == 200

    ret = resp.json['dataset']
    assert ret['dataset_id'] == ds.id


def test_get_datasets(app):
    ds1 = _add_dataset()
    ds2 = _add_dataset()

    resp = app.get('/api/renom_rg/datasets')

    assert resp.status_int == 200

    ret = resp.json['datasets']
    assert set(ds['dataset_id'] for ds in ret) >= {ds1.id, ds2.id}


def _add_searcher():
    searcher = db.ParamSearcher()
    session = db.session()
    session.add(searcher)
    session.commit()
    return searcher

DEFAULT_ALGORITHM_PARAMS = {'train_count': 5, 'valid_count': 5,
                            'target_train': [], 'target_valid': [], 'train_index': [1, 2, 3, 4, 5],
                            'valid_index': [6, 7, 8, 9, 10],
                            'num_neighbors': 5,
                            'fc_unit': [100, 50],
                            'channels': [10, 20, 20],
                            'script_file_name': 'userdefmodel.py'
                            }


def _add_model(algorithm=1, algorithm_params=dict(DEFAULT_ALGORITHM_PARAMS), dataset=None, searcher=None):
    if dataset is None:
        dataset = _add_dataset()

    model = db.Model(dataset_id=dataset.id, algorithm=algorithm,
                     algorithm_params=pickle.dumps(algorithm_params), batch_size=10,
                     epoch=10)

    session = db.session()
    session.add(model)
    session.commit()

    if searcher:
        searchermodel = db.ParamSearcherModel(searcher=searcher, model=model)
        session.add(searchermodel)
        session.commit()

    return model

def test_confirm(app, data_pickle):
    ds = _add_dataset()
    resp = app.post('/api/renom_rg/datasets/confirm', {
        'target_column_ids': '[]',
        'train_ratio': 0.8,
        'selected_scaling': 2})

    assert resp.status_code == 200
    print(resp.json)

def test_create_model(app):
    ds = _add_dataset()
    searcher = _add_searcher()
    resp = app.post('/api/renom_rg/models', {
        'dataset_id': ds.id,
        'algorithm': 1,
        'algorithm_params': json.dumps({'a': 1}),
        'batch_size': 10,
        'epoch': 10,
        'searcher_id': searcher.id
    })

    assert resp.status_int == 200
    model = db.session().query(db.Model).filter(db.Model.dataset_id == ds.id).one()
    assert model
    assert resp.json['model_id'] == model.id

    searchermodel = (db.session().query(db.ParamSearcherModel)
                     .filter(db.ParamSearcherModel.searcher_id == searcher.id)
                     .filter(db.ParamSearcherModel.model_id == model.id)).one()

    assert searchermodel


def test_delete_model(app):
    searcher = _add_searcher()
    model = _add_model(searcher=searcher)

    resp = app.delete('/api/renom_rg/models/%d' % model.id)

    assert resp.status_int == 200
    assert db.session().query(db.Model).filter(db.Model.id == model.id).count() == 0

    resp = app.delete('/api/renom_rg/models/%d' % model.id)
    assert resp.status_int == 404


def test_get_model(app):
    model = _add_model()
    resp = app.get('/api/renom_rg/models/%d' % model.id)

    assert resp.status_int == 200

    assert resp.json['model_id'] == model.id


def test_get_models(app):
    model1 = _add_model()
    model2 = _add_model()
    resp = app.get('/api/renom_rg/models')

    assert resp.status_int == 200

    ret = resp.json['models']
    assert set(model['model_id'] for model in ret) >= {model1.id, model2.id}


def test_model_deploy(app):
    model1 = _add_model()
    model1.deployed = 1

    model2 = _add_model()
    model2.deployed = 1

    session = db.session()
    session.add_all([model1, model2])
    session.commit()

    resp = app.post('/api/renom_rg/models/%s/deploy' % model2.id)

    assert resp.status_int == 200

    ret = resp.json['model']
    assert ret['model_id'] == model2.id
    assert ret['deployed'] == 1

    session = db.session()
    assert session.query(db.Model).get(model1.id).deployed == 0
    assert session.query(db.Model).get(model2.id).deployed == 1

    session.delete(model2)
    resp = app.post('/api/renom_rg/models/%s/deploy' % model2.id)
    assert resp.status_int == 404


@patch('renom_rg.server.server.train_task.train')
def test_train_model(train, app):
    model = _add_model()
    resp = app.get('/api/renom_rg/models/%s/train' % model.id)

    assert resp.status_int == 200
    assert resp.json['result'] == 'ok'


def test_get_running_models(app):
    model = _add_model()
    taskstate = train_task.TaskState.add_task(model)
    resp = app.get('/api/renom_rg/models/running')

    assert resp.status_int == 200

    found = next(s for s in resp.json['running_models'] if s['model_id'] == model.id)
    assert found


def test_wait_model_update_initial(app):
    model = _add_model()
    taskstate = train_task.TaskState.add_task(model)
    resp = app.get('/api/renom_rg/models/wait_model_update')

    assert resp.status_int == 200


def test_wait_model_update_nowait(app):
    model = _add_model()
    taskstate = train_task.TaskState.add_task(model)

    # wait_model_update returns immediately since serial defers.
    train_task.TaskState.serial = 0
    app.set_cookie('model_serial', '10')
    resp = app.get('/api/renom_rg/models/wait_model_update')

    assert resp.status_int == 200


def test_wait_model_update_wait(app):
    model = _add_model()
    taskstate = train_task.TaskState.add_task(model)

    def run_later():
        time.sleep(0.1)
        taskstate.signal()

    threading.Thread(target=run_later).start()
    # wait_model_update waits update
    train_task.TaskState.serial = 100
    app.set_cookie('model_serial', '100')
    resp = app.get('/api/renom_rg/models/wait_model_update')

    assert resp.status_int == 200
    assert resp.json['updated']


@patch('renom_rg.server.server.set_cuda_active')
@patch('renom_rg.server.server.use_device')
@patch('renom_rg.server.server.release_mem_pool')
def test_gpupool(set_cuda_active, use_device, release_mem_pool):
    gpupool = server.GPUPool(3)

    def f():
        import time
        from renom_rg.server.server import GPUPool

        time.sleep(0.01)
        return GPUPool.active_gpu.id

    with ThreadPoolExecutor() as e:
        all = set(e.map(gpupool.run, (f for _ in range(10))))
        assert all == {0, 1, 2}


def test_create_searcher(app):
    resp = app.post('/api/renom_rg/searchers', {
        'info': json.dumps({'a': 1}),
    })

    assert resp.status_int == 200
    id = resp.json['id']
    searcher = db.session().query(db.ParamSearcher).filter(db.ParamSearcher.id == id).one()
    assert searcher


def test_get_searcher(app):
    searcher = _add_searcher()
    model1 = _add_model(searcher=searcher)
    model2 = _add_model(searcher=searcher)

    resp = app.get('/api/renom_rg/searchers/%d' % searcher.id)
    assert resp.status_int == 200
    id = resp.json['id']
    assert searcher.id == id
    assert {model1.id, model2.id} == set(resp.json['model_ids'])


def test_get_searchers(app):
    searcher = _add_searcher()
    model1 = _add_model(searcher=searcher)
    model2 = _add_model(searcher=searcher)
    taskstate = train_task.TaskState.add_task(model1)

    searcher2 = _add_searcher()

    resp = app.get('/api/renom_rg/searchers')
    assert resp.status_int == 200

    dict1 = next(s for s in resp.json['searchers'] if s['id'] == searcher.id)
    assert set(dict1['model_ids']) == {model1.id, model2.id}
    assert set(d['model_id'] for d in dict1['taskstates']) == {model1.id}

    dict2 = next(s for s in resp.json['searchers'] if s['id'] == searcher2.id)
    assert not dict2['model_ids']
    assert not dict2['taskstates']


def test_delete_searcher(app):
    searcher = _add_searcher()
    model1 = _add_model(searcher=searcher)
    model2 = _add_model(searcher=searcher)

    resp = app.delete('/api/renom_rg/searchers/%d' % searcher.id)
    assert resp.status_int == 200

    resp = app.delete('/api/renom_rg/searchers/%d' % searcher.id)
    assert resp.status_int == 404

    q = db.session().query(db.Model).filter_by(id=model1.id).one()

    qq = db.session().query(db.ParamSearcherModel).filter_by(searcher_id=searcher.id).all()
    assert not qq

def test_train_usermodel(app, userscript, data_pickle):

    model = _add_model(algorithm=0xffffffff)

    taskstate = train_task.TaskState.add_task(model)

    train_task.train(taskstate, model.id)
