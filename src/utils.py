import pandas as pd
from datetime import datetime
from typing import List


def join_dfs(df_list: List, mode="left") -> pd.DataFrame:
    pdf = df_list[0]
    for df in df_list[1:]:
        pdf = pdf.join(df, mode)
    assert len(pdf) == len(df_list[0])
    return pdf


def day_of_week(date_str: str, pattern: str ="%m/%d/%Y") -> int:
    date_obj = datetime.strptime(date_str, pattern)
    return date_obj.weekday()  # 0 for Monday, 1 for Tuesday, ..., 6 for Sunday


def day_of_month(date_str: str) -> int:
    return int(date_str.split("/")[1])


def get_month(date_str) -> int:
    return int(date_str.split("/")[0])


def get_train_test_indexes(df: pd.DataFrame, test_size: float) -> tuple[List, List]:
    test_len = int(df.shape[0] * test_size)
    train_len = int(df.shape[0] - test_len)
    train_indexes = list(range(train_len))
    test_indexes = list(range(train_len, df.shape[0]))
    train_indexes = [list(df.index)[index] for index in train_indexes]
    test_indexes = [list(df.index)[index] for index in test_indexes]
    return train_indexes, test_indexes


def get_mean_std(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    means = df.mean(numeric_only=True)
    stds = df.std(numeric_only=True)
    return means, stds
