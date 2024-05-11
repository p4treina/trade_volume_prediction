import os
import numpy as np
import pandas as pd

from datetime import datetime
from typing import List


class DataExtractor():
    TARGETS = ["gm", "vix", "sp500", "gold", "eurusd", "bonds"]

    def __init__(self, path, target) -> None:
        self.path = path
        self.target = target

    def load_data(self) -> pd.DataFrame:
        root = os.path.dirname(os.getcwd())
        return pd.read_csv(f"{root}/{self.path}")

    def rename_columns(self, df: pd.DataFrame, target) -> pd.DataFrame:
        assert target in self.TARGETS, f"Invaid target: {target}"
        # rename columns to lower case
        df.columns = map(str.lower, df.columns)
        # Add _target to columns 
        if self.target == "gm":
            index = "business date"
        else:
            index = "date"
        new_columns = ["date"] + [column + f"_{target}" for column in df.columns if column != index]
        df.rename(columns=dict(zip(df.columns, new_columns)),inplace=True)
        # Remove space from column names
        df.columns = df.columns.str.replace(" ", "_")
        return df
    
    def extract_data(self) -> pd.DataFrame:
        df = self.load_data()
        df = self.rename_columns(df, self.target)
        df.set_index("date")
        return df

