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

    def __init__(self, process_reference):
        # собственный экземпляр конфига

        self.current_frame = None
        self.req_file_number_frames = None
        self.req_file_df = None
        self.config = Config()
        self.process_reference = process_reference
        # путь
        self.file_path = None
        self.file_name = None
        self.request_file = None

        # буфер для записи
        self.data_buf_list = []
        self.len_data_buf_list = 0
        self.data_buf_dict = {}
        self.len_data_buf_dict = 0
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

    def write_to_parquet_from_dict(self, data: dict):
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
            self.create_work_folder()
            self.create_file_name(self.data_buf_dict.get('Time')[0],
                                  self.data_buf_dict.get('Time')[-self.config.OUT_FRAME_HEIGHT])

            # print('start write parquet')
            # start_time = time.time()

            self.len_data_buf_dict = 0

            df = pd.DataFrame.from_dict(data=self.data_buf_dict, orient='columns')
            self.data_buf_dict.clear()

            df.to_parquet(rf"{self.file_path}/{self.file_name}")

            self.config_data_buf()
            return None
            # return f'parquet writer need {time.time() - start_time}s for {self.config.BUFFER_SIZE} img'
        return None

    def get_parquet_file_metadata(self, parquet_file_name):
        self.request_file = parquet_file_name
        print(f"запрос получен открываю файл {parquet_file_name}")
        self.req_file_df = pd.read_parquet(parquet_file_name)
        self.req_file_number_frames = int(len(self.req_file_df.index) / self.config.OUT_FRAME_HEIGHT)
        time_first_frame = self.req_file_df.iloc[0, 0]
        time_last_frame = self.req_file_df.iloc[self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1), 0]
        length_first_frame = self.req_file_df.iloc[0, 1]
        length_last_frame = self.req_file_df.iloc[self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1), 1]
        pos_uzk_first_frame = self.req_file_df.iloc[0, 2]
        pos_uzk_last_frame = self.req_file_df.iloc[self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1), 2]
        ret_dict = {'number_frames': self.req_file_number_frames, 'time_first_frame': time_first_frame,
                    'time_last_frame': time_last_frame, 'length_first_frame': length_first_frame,
                    'length_last_frame': length_last_frame, 'pos_UZK_first_frame': pos_uzk_first_frame,
                    'pos_UZK_last_frame': pos_uzk_last_frame}
        self.current_frame = 0
        self.process_reference.ret_parquet_file_metadata(ret_dict)

    def get_img_and_data_from_parquet(self):
        ret_dict = {'Image id': None, 'Image': None, 'That is all': False}
        image = self.req_file_df['Image'].iloc[self.current_frame * 512:self.current_frame * 512 + 512].values
        self.current_frame += 1
        ret_dict['Image id'] = self.current_frame
        ret_dict['Image'] = image
        if self.current_frame < self.req_file_number_frames:
            ret_dict['That is all'] = False
            return ret_dict
        else:
            ret_dict['That is all'] = True
            return ret_dict

    def read_from_parquet_to_img(self, parquet_file_name: str = ''):

        time_data = []
        zones_data = []
        time_dt = []

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
        self.file_path = f"{self.config.WORKING_DIRECTORY}/{datetime.datetime.now().year}/{datetime.datetime.now().month}/" \
                         f"{datetime.datetime.now().day}/{datetime.datetime.now().hour}"
        Path(self.file_path).mkdir(parents=True, exist_ok=True)

    def create_file_name(self, start_time, end_time):
        self.file_name = f"{datetime.datetime.fromtimestamp(start_time).strftime('%M-%S')}-{datetime.datetime.fromtimestamp(end_time).strftime('%M-%S')}.parquet"


if __name__ == '__main__':
    pass
