"""
Copyright 2019, Grid.

This source code is licensed under the ReNom Subscription Agreement, version 1.0.
ReNom Subscription Agreement Ver. 1.0 (https://www.renom.jp/info/license/index.html)
"""

import os

# Constants
# Algorithms
C_GCNN = 0
Kernel_GCNN = 1
DBSCAN_GCNN = 2
RANDOM_FOREST = 3
XGBOOST = 4
USER_DEFINED = 0xffffffff

# Directories
DATASRC_DIR = "datasrc"
DATASRC_PREDICTION = os.path.join(DATASRC_DIR, "prediction_set")
DATASRC_PREDICTION_OUT = os.path.join(DATASRC_DIR, "prediction_set", "output")
SCRIPT_DIR = "scripts"

# DB directories
DB_DIR = "storage"
DB_DIR_TRAINED_WEIGHT = os.path.join(DB_DIR, "trained_weight")
DB_DIR_ML_MODELS = os.path.join(DB_DIR, "ml_models")
