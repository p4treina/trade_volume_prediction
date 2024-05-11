import pandas as pd
from typing import List
from src.utils import get_month, day_of_week, day_of_month


class DataTransformer():

    @staticmethod
    def add_target(df: pd.DataFrame, column:str = "volume_gm" ) -> pd.DataFrame:
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
            df:pd.DataFrame,
            cols: List[str],
            periods: List[int] = [1, 2, 3]
        ) -> tuple[pd.DataFrame, List]:
        lags_columns = []
        for col in cols:
            for lag in periods:
                feature_col_name = f"{col}_lag_{lag}"
                df[feature_col_name] = df.shift(lag)[col]
                lags_columns.append(feature_col_name)
        return df, lags_columns

    @staticmethod
    def cap_outliers(df: pd.DataFrame, columns, means, stds, std_num=4):
        for column in columns:
            up_border = means[column] + std_num * stds[column]
            down_border = max(0, means[column] - std_num * stds[column])
            df[column] = df[column].clip(lower=down_border, upper=up_border)
        return df

    @staticmethod
    def add_target_rolling_mean(df: pd.DataFrame, target_column) -> pd.DataFrame:
        df['rolling_mean'] = df[target_column].rolling(window=3).mean()
        return df


    def transform(self):
        pass
