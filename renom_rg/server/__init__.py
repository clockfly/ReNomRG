import os

# Constants
# Algorithms
C_GCNN = 0
Kernel_GCNN = 1
DBSCAN_GCNN = 2
USER_DEFINED = 0xffffffff

# Directories
DATASRC_DIR = "datasrc"
DATASRC_PREDICTION = os.path.join(DATASRC_DIR, "prediction_set")
SCRIPT_DIR = "scripts"

# DB directories
DB_DIR = "storage"
DB_DIR_TRAINED_WEIGHT = os.path.join(DB_DIR, "trained_weight")
