import pickle
import os
import renom as rm
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from . import train_task
from . import DB_DIR_ML_MODELS, RANDOM_FOREST, XGBOOST

def random_forest(session, modeldef, n_estimators, max_depth,
                  X_train, y_train, X_valid, y_valid):
    if modeldef.algorithm == RANDOM_FOREST:
        regr = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
        filename = 'rf_' + str(modeldef.id) + '.pickle'
    elif modeldef.algorithm == XGBOOST:
        regr = xgb.XGBRegressor(n_estimators=n_estimators, max_depth=max_depth)
        filename = 'xgb_' + str(modeldef.id) + '.pickle'

    if y_train.shape[1] == 1:
        model = regr.fit(X_train, y_train.ravel())
    else:
        model = regr.fit(X_train, y_train)

    train_predicted = model.predict(X_train)
    train_predicted = train_predicted.reshape(-1, y_train.shape[1])
    predicted = model.predict(X_valid)
    predicted = predicted.reshape(-1, y_valid.shape[1])

    modeldef = train_task.prediction_sample_graph(modeldef, predicted, y_valid,
                                                  train_predicted, y_train)
    if not os.path.isdir(DB_DIR_ML_MODELS):
        os.makedirs(DB_DIR_ML_MODELS)
    filepath = os.path.join(DB_DIR_ML_MODELS, filename)
    with open(filepath, mode='wb') as f:
        pickle.dump(model, f)

    valid_loss = rm.mse(predicted, y_valid)

    feature_importances = model.feature_importances_.astype(float)
    modeldef.importances = pickle.dumps(np.round(feature_importances, 3).tolist())

    train_task.update_model(session, modeldef, predicted, y_valid, None,
                            valid_loss, None, filename)
