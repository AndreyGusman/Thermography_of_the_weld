import time
import pandas as pd

from src.config import Config
from src.data_format import DataFormat


# TODO прописать правила создания рабочей деректории DB(рабочая папка, разбиение по часам, формирование имён паркетных файлов)
class ParquetWorker:

    def __init__(self):
        self.data_buf_list = []
        self.len_data_buf_list = 0
        self.data_buf_dict = {}
        self.len_data_buf_dict = 0
        self.config = Config()
        self.config_data_buf()

    def write_to_parquet_from_list(self, data: list, title: list, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        self.data_buf_list.append(data)
        self.len_data_buf_list += 1
        if self.len_data_buf_list >= self.config.BUFFER_SIZE:
            self.len_data_buf_list = 0
            start_time = time.time()
            df = pd.DataFrame([self.data_buf_list[0]], columns=title)
            for i in range(1, len(self.data_buf_list)):
                df.loc[len(df.index)] = self.data_buf_list[i]
            df.to_parquet(path=f"{self.config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
            self.data_buf_list.clear()
            return f'parquet writer need {time.time() - start_time}s for {self.config.BUFFER_SIZE} img'
        return None

    def write_to_parquet_from_dict(self, data: dict, parquet_file_path: str = '',
                                   parquet_file_name: str = 'db.parquet'):
        # записываем входящие значения
        for key in data:
            if key != 'Image':
                self.data_buf_dict[key].append(data[key])
            else:
                # раскладываем картинку построчно

                for line in range(512):
                    self.data_buf_dict[key].append(data[key][line])

        # выравниваем длину столбцов
        for key in self.data_buf_dict:
            if key != 'Image':
                for i in range(511):
                    self.data_buf_dict[key].append(0)

        self.len_data_buf_dict += 1
        if self.len_data_buf_dict >= self.config.BUFFER_SIZE:
            print('start write parquet')
            start_time = time.time()
            self.len_data_buf_dict = 0
            df = pd.DataFrame.from_dict(data=self.data_buf_dict, orient='columns')
            df.to_parquet(f"{self.config.WORKING_DIRECTORY}{parquet_file_path}{parquet_file_name}")
            self.data_buf_dict.clear()
            self.config_data_buf()
            return f'parquet writer need {time.time() - start_time}s for {self.config.BUFFER_SIZE} img'
        return None

    def config_data_buf(self):
        if self.config.PARQUET_MODE == 1:
            var_name_list = DataFormat.parquet_format_mode_1.copy()
            self.data_buf_dict = {var_name: [] for var_name in var_name_list}
        if self.config.PARQUET_MODE == 2:
            var_name_list = DataFormat.parquet_format_mode_2.copy()
            self.data_buf_dict = {var_name: [] for var_name in var_name_list}
        if self.config.PARQUET_MODE == 3:
            var_name_list = DataFormat.parquet_format_mode_3.copy()
            self.data_buf_dict = {var_name: [] for var_name in var_name_list}


if __name__ == '__main__':
    pass
