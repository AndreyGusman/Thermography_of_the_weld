import time
import datetime
import pandas as pd
from pathlib import Path
from src.config import Config
from src.data_format import DataFormat


class ParquetWriter:

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

    def add_dict_to_buf(self, data: dict):
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
            return self.write_parquet_from_dict()
        return None

    def write_parquet_from_dict(self):
        self.create_work_folder()
        self.create_file_name(self.data_buf_dict.get('Time')[0],
                              self.data_buf_dict.get('Time')[-self.config.OUT_FRAME_HEIGHT])

        print('start write parquet')
        start_time = time.time()

        self.len_data_buf_dict = 0

        df = pd.DataFrame.from_dict(data=self.data_buf_dict, orient='columns')
        self.data_buf_dict.clear()

        df.to_parquet(rf"{self.file_path}/{self.file_name}")

        self.config_data_buf()
        # return None
        return f' need {time.time() - start_time}s for {self.config.BUFFER_SIZE} img'

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
