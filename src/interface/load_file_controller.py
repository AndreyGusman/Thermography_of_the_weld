from src.interface.loaded_parquet_file import LoadedParquetFile
from src.interface.parquet_analyser import ParquetAnalyser


class LoadFileController:
    def __init__(self, screen_reference, process_reference):
        self.screen_reference = screen_reference
        self.process_reference = process_reference

        self.current_view_pq_file = LoadedParquetFile(self.screen_reference, is_current_file=True)
        self.next_view_pq_file = LoadedParquetFile(self.screen_reference)
        self.previous_view_pq_file = LoadedParquetFile(self.screen_reference)

        self.parquet_analyser = ParquetAnalyser()

    def associate_img_and_plc_data(self, img_data):
        file_name = img_data.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.associate_img_and_plc_data(img_data)
            if self.current_view_pq_file.is_loaded and self.next_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.next_view_pq_file.file_name)

        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.associate_img_and_plc_data(img_data)
            if self.next_view_pq_file.is_loaded and self.previous_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.previous_view_pq_file.file_name)

        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.associate_img_and_plc_data(img_data)

    def set_metadata(self, metadata: dict):
        file_name = metadata.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.set_metadata(metadata)
            self.screen_reference.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.set_metadata(metadata)
            self.screen_reference.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.set_metadata(metadata)
            self.screen_reference.set_text_parquet_info(text=f'Получены метаданные файла {file_name}')
        # self.ScrollBar_Parquet.setMaximum(self.metadata['number_frames'])

    def set_plc_data(self, plc_data):
        file_name = plc_data.pop('File name')
        if file_name == self.current_view_pq_file.file_name:
            self.current_view_pq_file.set_plc_data(plc_data)
            self.screen_reference.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')
        elif file_name == self.next_view_pq_file.file_name:
            self.next_view_pq_file.set_plc_data(plc_data)
            self.screen_reference.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')
        elif file_name == self.previous_view_pq_file.file_name:
            self.previous_view_pq_file.set_plc_data(plc_data)
            self.screen_reference.set_text_parquet_info(text=f'Получены данные ПЛК файла {file_name}')

    def replace_previous_file(self):
        if isinstance(self.previous_view_pq_file.file_name, str) and \
                isinstance(self.previous_view_pq_file.metadata, dict) and \
                isinstance(self.previous_view_pq_file.image_and_plc_data, dict):
            self.screen_reference.set_text_parquet_info(
                text=f'Подгружен предыдущий parquet файл {self.previous_view_pq_file.file_name}')

            data1, data2, data3 = self.current_view_pq_file.get_all_data()
            self.next_view_pq_file.set_all_data(data1, data2, data3)

            data1, data2, data3 = self.previous_view_pq_file.get_all_data()
            self.current_view_pq_file.set_all_data(data1, data2, data3)

            last_key = list(self.current_view_pq_file.image_and_plc_data.keys())[-1]
            last_key = last_key.split(' ')[-1]
            self.screen_reference.ScrollBar_Parquet.setMaximum(int(last_key))
            if self.current_view_pq_file.is_loaded:
                self.screen_reference.ScrollBar_Parquet.setValue(
                    self.current_view_pq_file.metadata.get('number_frames'))
                self.screen_reference.show_img()

            self.previous_view_pq_file.clear_data()
            _, self.previous_view_pq_file.file_name = self.parquet_analyser.check_neighboring_file(
                self.current_view_pq_file.file_name)
            if self.previous_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.previous_view_pq_file.file_name)
        else:
            self.screen_reference.hmi_reference.show_message(title='Внимание!',
                                                             message='Предыдущего parquet файла не существует')

    def replace_next_file(self):
        if isinstance(self.next_view_pq_file.file_name, str) and \
                isinstance(self.next_view_pq_file.metadata, dict) and \
                isinstance(self.next_view_pq_file.image_and_plc_data, dict):
            self.screen_reference.set_text_parquet_info(
                text=f'Подгружен следующий parquet файл {self.next_view_pq_file.file_name}')

            data1, data2, data3 = self.current_view_pq_file.get_all_data()
            self.previous_view_pq_file.set_all_data(data1, data2, data3)

            data1, data2, data3 = self.next_view_pq_file.get_all_data()
            self.current_view_pq_file.set_all_data(data1, data2, data3)

            last_key = list(self.current_view_pq_file.image_and_plc_data.keys())[-1]
            last_key = last_key.split(' ')[-1]
            self.screen_reference.ScrollBar_Parquet.setMaximum(int(last_key))
            if self.current_view_pq_file.is_loaded:
                self.screen_reference.ScrollBar_Parquet.setValue(1)
                self.screen_reference.show_img()

            self.next_view_pq_file.clear_data()
            self.next_view_pq_file.file_name, _ = self.parquet_analyser.check_neighboring_file(
                self.current_view_pq_file.file_name)
            if self.next_view_pq_file.file_name is not None:
                self.process_reference.get_parquet_file(self.next_view_pq_file.file_name)
        else:
            self.screen_reference.hmi_reference.show_message(title='Внимание!',
                                                             message='Следующего parquet файла не существует')

    def check_file_is_load(self, file_path):
        if file_path == self.current_view_pq_file.file_name:
            print('file is load')
            return
        else:

            if file_path == self.previous_view_pq_file.file_name:
                if isinstance(self.previous_view_pq_file.file_name, str) and \
                        isinstance(self.previous_view_pq_file.metadata, dict) and \
                        isinstance(self.previous_view_pq_file.image_and_plc_data, dict):
                    self.replace_previous_file()
                    print('load prev file')
                    return

            if file_path == self.next_view_pq_file.file_name:
                if isinstance(self.next_view_pq_file.file_name, str) and \
                        isinstance(self.next_view_pq_file.metadata, dict) and \
                        isinstance(self.next_view_pq_file.image_and_plc_data, dict):
                    self.replace_next_file()
                    print('load next file')
                    return

            self.process_reference.get_parquet_file(file_path)
            self.screen_reference.set_text_parquet_info(text=f'Создан запрос на чтение файда {file_path}')
            self.current_view_pq_file.file_name = file_path
            self.next_view_pq_file.file_name, self.previous_view_pq_file.file_name = self.parquet_analyser.check_neighboring_file(
                file_path)
            print('load new file')
            return
