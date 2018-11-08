import pickle
import random
import json
from renom_rg.server import db
from renom_rg.server import server
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


def test_get_labels(app):
    resp = app.get('/api/renom_rg/datasets/labels')

    assert resp.status_int == 200
    assert resp.json['labels']


def test_create_dataset(app):
    resp = app.post('/api/renom_rg/datasets', {
        'name': 'test_create_dataset_1',
        'description': 'description',
        'target_column_id': 10,
        'labels': json.dumps([1, 2, 3, 4]),
        'train_ratio': 0.1,
        'train_index': json.dumps([5, 6]),
        'valid_index': json.dumps([7, 8]),
    })

    assert resp.status_int == 200
    q = db.session().query(db.DatasetDef)
    ds = q.filter(db.DatasetDef.name == 'test_create_dataset_1').one()
    assert ds

def _add_dataset():
    name = str(random.random())
    ds = db.DatasetDef(name=name, description='description',
                       target_column_id=1, labels=pickle.dumps([1, 2, 3]),
                       train_ratio=0.1, train_index=pickle.dumps([2, 3, 4]),
                       valid_index=pickle.dumps([3, 4, 5]))

    session = db.session()
    session.add(ds)
    session.commit()
    return ds

def test_delete_dataset(app):
    ds = _add_dataset()
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


def _add_model():
    ds = _add_dataset()
    model = db.Model(dataset_id=ds.id, algorithm=1,
                     algorithm_params=pickle.dumps(None), batch_size=10,
                     epoch=10)

    session = db.session()
    session.add(model)
    session.commit()
    return model

def test_create_model(app):
    ds = _add_dataset()
    resp = app.post('/api/renom_rg/models', {
        'dataset_id': ds.id,
        'algorithm': 1,
        'algorithm_params': json.dumps({'a': 1}),
        'batch_size': 10,
        'epoch': 10,
    })

    assert resp.status_int == 200
    model = db.session().query(db.Model).filter(db.Model.dataset_id == ds.id).one()
    assert model


def test_delete_model(app):
    model = _add_model()
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
