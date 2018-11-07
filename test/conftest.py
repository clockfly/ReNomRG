# content of a/conftest.py
import sys
import traceback
import pytest
import tempfile
import shutil

import bottle
from bottle import default_app
from webtest import TestApp
from sqlalchemy import create_engine

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

