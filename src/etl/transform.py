from typing import List

import pandas as pd

from utils import day_of_month, day_of_week, get_month


class DataTransformer:
    @staticmethod
    def add_target(df: pd.DataFrame, column: str = "volume_gm") -> pd.DataFrame:
        df["target"] = df[column].shift(-1)
        return df

    @staticmethod
    def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
        df["day_of_week"] = list(map(day_of_week, df.index.tolist()))
        df["day_of_month"] = list(map(day_of_month, df.index.tolist()))
        df["month"] = list(map(get_month, df.index.tolist()))
        return df

    @staticmethod
    def add_lags(
        df: pd.DataFrame, cols: List[str], periods: List[int] = [1, 2, 3]
    ) -> tuple[pd.DataFrame, List]:
        for col in cols:
            for lag in periods:
                feature_col_name = f"{col}_lag_{lag}"
                df[feature_col_name] = df.shift(lag)[col]
        return df

    @staticmethod
    def cap_outliers(df: pd.DataFrame, columns, means, stds, std_num=4):
        for column in columns:
            up_border = means[column] + std_num * stds[column]
            down_border = max(0, means[column] - std_num * stds[column])
            df[column] = df[column].clip(lower=down_border, upper=up_border)
        return df

    @staticmethod
    def add_target_rolling_mean(df: pd.DataFrame, target_column) -> pd.DataFrame:
        df["rolling_mean"] = df[target_column].rolling(window=3).mean()
        return df

    def transform(self, df: pd.DataFrame, means, stds) -> pd.DataFrame:
        # Remove null values with interpolation
        cols = ["volume_gm"]
        # df = df.interpolate()
        # Cap outliers
        df = self.cap_outliers(df, cols, means, stds)
        # Add rolling mean value
        df = self.add_target_rolling_mean(df, "target")
        # Add lag
        df = self.add_lags(df, ["volume_gm"], [1])
        return df
