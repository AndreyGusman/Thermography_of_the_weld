import time
import pandas as pd

from src.config import Config


class ParquetWorker:

    def __init__(self):
        self.data_buf = []
        self.config = Config()

    def write_to_parquet_from_list(self, data: list, title: list, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        self.data_buf.append(data)
        if len(self.data_buf) >= self.config.BUFFER_SIZE:
            start_time = time.time()
            df = pd.DataFrame([self.data_buf[0]], columns=title)
            for i in range(1, len(self.data_buf)):
                df.loc[len(df.index)] = self.data_buf[i]
            df.to_parquet(path=f"{self.config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
            self.data_buf.clear()
            return f'parquet writer need {time.time() - start_time}s for {self.config.BUFFER_SIZE} img'
        return None

    def write_to_parquet_from_dict(self, data: dict, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        df = pd.DataFrame(data)
        df.to_parquet(f"{self.config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
