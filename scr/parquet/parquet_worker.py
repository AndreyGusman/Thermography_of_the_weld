import time

import scr.config as config

import pyarrow.parquet as pq
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import random


class ParquetWorker:

    def __init__(self):
        self.data_buf = []

    def write_to_parquet_from_list(self, data: list, title: list, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        self.data_buf.append(data)
        if len(self.data_buf) > 49:

            df = pd.DataFrame([self.data_buf[0]], columns=title)
            for i in range(1, len(self.data_buf)):
                df.loc[len(df.index)] = self.data_buf[i]
            start_time = time.time()
            df.to_parquet(f"{config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
            print(f'parquet write need {time.time() - start_time}s')
            self.data_buf.clear()

    @staticmethod
    def write_to_parquet_from_dict(data: dict, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        df = pd.DataFrame(data)
        df.to_parquet(f"{config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
