import os
import time
import datetime
import pandas as pd
import numpy as np
from pathlib import Path
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

                for line in range(self.config.WIDTH_IMAGE):
                    self.data_buf_dict[key].append(data[key][line])

        # выравниваем длину столбцов
        for key in self.data_buf_dict:
            if key != 'Image':
                for i in range(self.config.WIDTH_IMAGE - 1):
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

    def read_from_parquet_to_img(self, parquet_file_name: str = '', img_file_path: str = ''):

        time_data = []
        zones_data = []
        time_dt = []

        df = pd.read_parquet((parquet_file_name), columns=['Time', 'Length', 'Pos_UZK'])
        number_frames = int(len(df.index) / (640))
        time_first_frame = df.iloc[0, 0]
        time_last_frame = df.iloc[number_frames, 0]
        length_first_frame = df.iloc[0, 1]
        length_last_frame = df.iloc[number_frames, 1]
        pos_UZK_first_frame = df.iloc[0, 2]
        pos_UZK_last_frame = df.iloc[number_frames, 2]
        print()

        for i in range(0, int(((pd.read_parquet(parquet_file_name, columns=['Zones']).count()) / (
                self.config.WIDTH_IMAGE)))):
            df = pd.read_parquet((parquet_file_name), columns=['Zones', 'Time'])
            time_data.append(df.iloc[i * self.config.WIDTH_IMAGE, 1])
            data_buf = []
            if i == 0:
                j = 0
                while j <= self.config.WIDTH_IMAGE:
                    data_buf.append(df.iloc[j, 0])
                    j += 1
            else:
                j = 1
                while j <= (self.config.WIDTH_IMAGE + 1):
                    data_buf.append(df.iloc[j + (i * self.config.WIDTH_IMAGE), 0])
                    j += 1
            np.array(zones_data.append((np.array(data_buf))))

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

    def create_work_folder(self):
        file_path = f"{datetime.datetime.now().year}/{datetime.datetime.now().month}/" \
                    f"{datetime.datetime.now().day}/{datetime.datetime.now().hour}"
        Path(file_path).mkdir(parents=True, exist_ok=True)
        file_name = str(datetime.datetime.now().strftime("%M") + ".parquet")


if __name__ == '__main__':
    pass
