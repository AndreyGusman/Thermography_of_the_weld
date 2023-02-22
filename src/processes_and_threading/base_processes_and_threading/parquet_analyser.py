import glob
from natsort import natsorted
from src.config import Config


class ParquetAnalyser:
    def __init__(self):
        self.sorted_file_path_list = None
        self.dict_parquet_file = None
        self.update_dict_parquet_files()

    def update_sorted_file_path_list(self):
        file_pattern = Config.WORKING_DIRECTORY + '/*' + '/*' + '/*' + '/*' + '/*.parquet'
        file_path_list = glob.glob(file_pattern)
        for i in range(len(file_path_list)):
            file_path_list[i] = file_path_list[i].replace('\\', '/')
        file_path_list = natsorted(file_path_list)
        self.sorted_file_path_list = file_path_list

    def update_dict_parquet_files(self):
        self.update_sorted_file_path_list()
        self.dict_parquet_file = {self.sorted_file_path_list[i]: i for i in range(len(self.sorted_file_path_list))}

    def check_neighboring_file(self, file_name):
        number_current_file = self.dict_parquet_file.get(file_name)
        invert_dict = dict(zip(self.dict_parquet_file.values(), self.dict_parquet_file.keys()))
        next_file = invert_dict.get(number_current_file+1)
        previous_file = invert_dict.get(number_current_file-1)
        return next_file, previous_file
