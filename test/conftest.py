"""
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
"""

# content of a/conftest.py
import os
import sys
import traceback
import pytest
import tempfile
import shutil

import bottle
from bottle import default_app
from webtest import TestApp
from sqlalchemy import create_engine, event

import renom_rg.server.server
import renom_rg.server.db


class SaneTestApp(TestApp):
    def _check_status(self, status, res):
        # don't check status by default
        pass

    def _check_errors(self, res):
        # don't steal application's error message
        errors = res.errors
        if errors:
            print(res.errors, file=sys.stderr)


bottle.debug(True)


@pytest.fixture(scope="session", autouse=True)
def session():
    dirname = tempfile.mkdtemp()
    engine = create_engine('sqlite:///%s/storage.db' % dirname, echo=True)
    event.listen(engine, 'connect', renom_rg.server.db.set_fk_constrain)

    renom_rg.server.db.Base.metadata.create_all(engine)
    renom_rg.server.db.initsession(engine)

    try:
        yield 1
    finally:
        try:
            engine.dispose()
        except Exception:
            traceback.print_exc()

        try:
            shutil.rmtree(dirname, ignore_errors=True)
        except Exception:
            traceback.print_exc()


@pytest.fixture
def app():
    app = renom_rg.server.server.get_app()
    app.catchall = False  # raise exception on error
    return SaneTestApp(app)


@pytest.fixture
def sitedir(tmpdir):
    d = tmpdir.mkdir('site')

    d.mkdir('datasrc')
    d.mkdir('scripts')
    d.mkdir('storage')
    d.mkdir('storage/trained_weight')

    cwd = d.chdir()

    try:
        yield d
    finally:
        cwd.chdir()


@pytest.fixture
def data_pickle(sitedir):
    datasrc = sitedir.join('datasrc')
    pickefile = os.path.join(os.path.split(__file__)[0], 'data.pickle')
    with open(pickefile, 'rb') as f:
        datasrc.join('data.pickle').write_binary(f.read())

@pytest.fixture
def userscript(sitedir):
    datasrc = sitedir.join('scripts')
    srcfile = os.path.join(os.path.split(__file__)[0], 'userdefmodel.py')
    with open(srcfile) as f:
        datasrc.join('userdefmodel.py').write(f.read())
