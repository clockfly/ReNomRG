import os

# Constants
# Algorithms
C_GCNN = 0
Kernel_GCNN = 1
DBSCAN_GCNN = 2

# model state
STATE_RESERVED = 0
STATE_RUNNING = 1
STATE_FINISHED = 2
STATE_DELETED = 3

# Model running state
RUN_STATE_TRAINING = 0
RUN_STATE_VALIDATING = 1
RUN_STATE_PREDICTING = 2
RUN_STATE_STARTING = 3
RUN_STATE_STOPPING = 4

# Thread
MAX_THREAD_NUM = 2
GPU_NUM = 0

try:
    import renom.cuda
    if renom.cuda.has_cuda():
        MAX_THREAD_NUM = GPU_NUM = renom.cuda.cuGetDeviceCount()
except Exception:
    pass

# Directories
DATASRC_DIR = "datasrc"
DATASRC_PREDICTION = os.path.join(DATASRC_DIR, "prediction_set")

# DB directories
DB_DIR = "storage"
DB_DIR_TRAINED_WEIGHT = os.path.join(DB_DIR, "trained_weight")

def create_dirs():
    # Create directories
    for path in [DATASRC_PREDICTION, DB_DIR_TRAINED_WEIGHT]:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Directory %s is newly created." % (path))
