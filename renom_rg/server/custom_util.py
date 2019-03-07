"""
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
"""

import os
from renom_rg.server import SCRIPT_DIR

def _load_usermodel(algorithm_params):
    script = algorithm_params['script_file_name']

    scriptdir = os.path.abspath(SCRIPT_DIR)
    if not scriptdir.endswith(os.path.sep):
        scriptdir += os.path.sep

    scriptfile = os.path.abspath(os.path.join(scriptdir, script))
    if not scriptfile.startswith(scriptdir):
        raise ValueError('Invalid script name: %s' % scriptfile)
    elif not os.path.exists(scriptfile):
        raise ValueError('Invalid script name: %s' % scriptfile)

    scr = open(scriptfile).read()
    d = {}
    exec(scr, d)
    builder = d['create_model']
    return builder(algorithm_params)
