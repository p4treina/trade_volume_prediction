import os

ROOT_DIR = os.getcwd()
VOLUME_DATA_PATH = "data/VOLUMES.csv"
FEATURES = ["rolling_mean", "volume_gm_lag_1", "volume_gm"]
MODEL_NAME = "xgboost_pipeline"
MODELS_PATH = f"{ROOT_DIR}/models"
RANDOM_STATE = 42
