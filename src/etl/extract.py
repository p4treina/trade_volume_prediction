import os
import pandas as pd
from typing import List


class DataExtractor():
    def __init__(self, path, target) -> None:
        self.path = path
        self.target = target

    def load_data(self) -> pd.DataFrame:
        root = os.path.dirname(os.getcwd())
        return pd.read_csv(f"{root}/{self.path}")

    def rename_columns(self, df: pd.DataFrame, target) -> pd.DataFrame:
        # rename columns to lower case
        df.columns = map(str.lower, df.columns)
        # Add _target to columns
        date_col = "business date"
        new_columns = ["date"] + [column + f"_{target}" for column in df.columns if column != date_col]
        df.rename(columns=dict(zip(df.columns, new_columns)),inplace=True)
        # Remove space from column names
        df.columns = df.columns.str.replace(" ", "_")
        return df
    
    @staticmethod
    def remove_constant_period(df: pd.DataFrame, date_begin: str ="4/1/2023", date_end: str ="5/29/2023") -> pd.DataFrame:
        left_index: int =list(df.index).index(date_begin) 
        right_index: int = list(df.index).index(date_end) + 1
        df = df.drop(df.index[left_index:right_index])
        return df

    def extract_data(self) -> pd.DataFrame:
        df = self.load_data()
        df = self.rename_columns(df, self.target)
        df = self.remove_constant_period(df)
        df = df.set_index("date")
        return df
