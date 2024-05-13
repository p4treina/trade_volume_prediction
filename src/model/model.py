import pickle
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict

import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


# adding comment to trigger pre-commit#
class ModelIsNone(Exception):
    """
    Raised when trying to predict or evaluate a model that is None
    """

    pass


class Model(ABC):
    """
    Abstract class that defines a common interface for model classes

    Raises:
        ModelIsNone: Exception raised when trying to fit or predict a
        model that has not being trained or loaded from MLflow
    """

    MODEL_NONE_ERROR_MSG = "The model is neither trained nor loaded from mlflow"
    WRONG_MODEL_PATH = "The provided path does not exists"

    def __init__(
        self,
    ) -> None:
        """

        Args:
            categorical_features (Union[List[str], None]): Column names of the categorical features
            numeric_features (Union[List[str], None]): Column names of the numeic features
        """
        self._model: Pipeline | None = None

    @property
    def model(self):
        return self._model

    @abstractmethod
    def fit(
        self,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
    ):
        pass

    @abstractmethod
    def predict(self, x: pd.DataFrame):
        pass

    @abstractmethod
    def evaluate(self, x: pd.DataFrame, y: pd.DataFrame) -> Dict:
        pass


class VolumeForecastModel(Model):
    """
    Class for Volume Forecast Model

    Raises:
        ModelIsNone: Exception raised when trying to fit or predict a
        model that has not being trained or loaded from MLflow
    """

    MODEL_NONE_ERROR_MSG = "The model is neither trained nor loaded"
    WRONG_MODEL_PATH = "The provided path does not exists"

    def __init__(
        self,
        learning_rate: float | None,
        max_depth: int | None,
        subsample: float | None,
        random_state: int | None,
    ) -> None:
        super().__init__()
        if (
            learning_rate is not None
            and max_depth is not None
            and subsample is not None
            and random_state is not None
        ):
            self._model = self._get_pipeline(
                learning_rate, max_depth, subsample, random_state
            )

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, path: str):
        """Loads model from path

        Args:
            path (str): Path to the model

        Raises:
            OSError: Raised when the path is incorrect
        """
        try:
            with open(path, "rb") as file:
                self._model: Pipeline = pickle.load(file)
        except OSError:
            raise OSError(self.WRONG_MODEL_PATH + f" {path}")

    def _get_pipeline(
        self,
        learning_rate: float = 0.2,
        max_depth: int = 5,
        subsample: float = 0.8,
        random_state: int = 42,
    ) -> Pipeline:
        preprocessor = Pipeline(
            steps=[
                ("scaler", MinMaxScaler()),
            ]
        )
        xgb_model = xgb.XGBRegressor(
            eval_metric=root_mean_squared_error,
            learning_rate=learning_rate,
            max_depth=max_depth,
            subsample=subsample,
            random_state=random_state,
        )
        return Pipeline(steps=[("preprocessor", preprocessor), ("model", xgb_model)])

    def fit(
        self,
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
    ):
        if self._model is None:
            raise ModelIsNone(self.MODEL_NONE_ERROR_MSG)
        self._model = self._model.fit(x_train, y_train)

    def predict(self, x: pd.DataFrame):
        """_summary_

        Args:
            x (pd.DataFrame): Input dataframe to predict

        Raises:
            ModelIsNone:

        Returns:
            Trained model
        """
        if self._model is None:
            raise ModelIsNone(self.MODEL_NONE_ERROR_MSG)
        predictions = self._model.predict(x)
        return predictions

    def evaluate(self, x: pd.DataFrame, y: pd.DataFrame) -> Dict:
        """_summary_

        Args:
            x (pd.DataFrame): Input
            y (pd.DataFrame): Ground truth

        Returns:
            Dict: dictionary with evaluation metrics
        """
        preds, _ = self.predict(x)
        metrics_dict: Dict = defaultdict()
        metrics_dict["MAE"] = mean_absolute_error(y, preds)
        metrics_dict["RMSE"] = root_mean_squared_error(y, preds)
        metrics_dict["R2"] = r2_score(y, preds)
        return metrics_dict
