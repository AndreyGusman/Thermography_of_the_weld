import pandas as pd
import numpy as np

from src.config import Config


class ParquetReader:

    def __init__(self, process_reference):

        self.config = Config()
        self.process_reference = process_reference

        self.current_frame = None
        self.req_file_number_frames = None
        self.req_file_df = None
        self.request_file = None

    def get_plc_data_from_parquet(self):
        ret_dict = {f'Image {i + 1}': {} for i in range(self.req_file_number_frames)}
        for key in ret_dict.keys():
            val_dict = {var_name: None for var_name in list(self.req_file_df)}
            key_spl = key
            frame_number = int(key_spl.split(' ')[1]) - 1
            for var_name in val_dict.keys():
                if var_name not in ['Image', 'Defect mask', 'type']:
                    val_dict[var_name] = self.req_file_df[var_name].iloc[frame_number * 512]
            ret_dict[key] = val_dict
        ret_dict['File name'] = self.request_file
        return ret_dict

    def get_parquet_file_metadata(self, parquet_file_name):
        self.request_file = parquet_file_name
        self.req_file_df = pd.read_parquet(parquet_file_name)
        self.req_file_number_frames = int(len(self.req_file_df.index) / self.config.OUT_FRAME_HEIGHT)
        time_first_frame = self.req_file_df['Time'].iloc[0]
        time_last_frame = self.req_file_df['Time'].iloc[
            self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1)]
        length_first_frame = self.req_file_df['Length'].iloc[0]
        length_last_frame = self.req_file_df['Length'].iloc[
            self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1)]
        pos_uzk_first_frame = self.req_file_df['Pos_UZK'].iloc[0]
        pos_uzk_last_frame = self.req_file_df['Pos_UZK'].iloc[
            self.config.OUT_FRAME_HEIGHT * (self.req_file_number_frames - 1)]
        ret_dict = {'number_frames': self.req_file_number_frames, 'time_first_frame': time_first_frame,
                    'time_last_frame': time_last_frame, 'length_first_frame': length_first_frame,
                    'length_last_frame': length_last_frame, 'pos_UZK_first_frame': pos_uzk_first_frame,
                    'pos_UZK_last_frame': pos_uzk_last_frame, 'File name': self.request_file}
        self.current_frame = 0
        self.process_reference.ret_parquet_file_metadata(ret_dict)

    def get_img_from_parquet(self):
        ret_dict = {'Image id': None, 'Image': None, 'That is all': False, 'File name': self.request_file
                    }
        image = np.vstack(self.req_file_df['Image'].iloc[
                          self.current_frame * self.config.OUT_FRAME_HEIGHT:self.current_frame * self.config.OUT_FRAME_HEIGHT + self.config.OUT_FRAME_HEIGHT].values)
        self.current_frame += 1

        ret_dict['Image id'] = self.current_frame
        ret_dict['Image'] = image
        if self.current_frame < self.req_file_number_frames:
            ret_dict['That is all'] = False
            return ret_dict
        else:
            ret_dict['That is all'] = True
            return ret_dict
