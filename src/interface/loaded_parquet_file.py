class LoadedParquetFile:
    def __init__(self, screen_reference, is_current_file=False):
        self.file_name = None
        self.metadata = None
        self.image_and_plc_data = {}
        self.is_current_file = is_current_file
        self.is_loaded = False
        self.screen_reference = screen_reference

    def set_metadata(self, metadata):
        self.metadata = metadata

    def set_plc_data(self, plc_data):
        self.image_and_plc_data = plc_data

    def associate_img_and_plc_data(self, img_data):
        try:
            self.image_and_plc_data[f'Image {img_data["Image id"]}']['Image'] = img_data['Image']
            self.screen_reference.set_text_parquet_info(text=f'Получен кадр №{img_data["Image id"]} из '
                                                             f'{self.metadata.get("number_frames")} '
                                                             f'parquet файла {self.file_name}')
        except KeyError:
            print(f"Image {img_data['Image id']} not associate")
            return

        if img_data["Image id"] == self.metadata.get('number_frames'):
            self.is_loaded = True
            print(f'file {self.file_name} loaded')
        else:
            self.is_loaded = False

        if self.is_current_file:
            self.screen_reference.ScrollBar_Parquet.setMaximum(img_data["Image id"])
            if img_data["Image id"] == 1:
                read_img_and_data = self.image_and_plc_data.get(f'Image {1}').copy()
                self.screen_reference.update_arch_img(read_img_and_data)
                self.screen_reference.ScrollBar_Parquet.setValue(1)
        return self.is_loaded

    def clear_data(self):
        self.file_name = None
        self.metadata = None
        self.image_and_plc_data = {}
        self.is_loaded = False

    def set_all_data(self, file_name, metadata: dict, image_and_plc_data: dict):
        if isinstance(file_name, str) and isinstance(metadata, dict) and isinstance(image_and_plc_data, dict):
            self.clear_data()
            self.file_name = file_name
            self.metadata = metadata.copy()
            self.image_and_plc_data = image_and_plc_data.copy()
            self.check_exist_last_image()
        else:
            print(
                f"input data failed validation, file_name {type(file_name)}, "
                f"metadata {type(metadata)}, image_and_plc_data {type(image_and_plc_data)}")

    def get_all_data(self):
        return self.file_name, self.metadata, self.image_and_plc_data

    def get_img_and_plc_data(self, key, select_img_id):
        if key != 'Image':
            if self.image_and_plc_data.get(key) is not None:
                read_img_and_data = self.image_and_plc_data.get(f'Image {select_img_id}').copy()
                if read_img_and_data['Image'] is not None:
                    self.screen_reference.update_arch_img(read_img_and_data)
                    self.screen_reference.set_text_parquet_info(text=f'Отображается кадр №{select_img_id} из '
                                                                     f'{self.metadata.get("number_frames")} файла '
                                                                     f'{self.file_name}')

    def check_exist_last_image(self):
        key = f'Image {self.metadata.get("number_frames")}'
        if self.image_and_plc_data.get(key) is not None:
            read_img_and_data = self.image_and_plc_data.get(f'Image {self.metadata.get("number_frames")}').copy()
            if read_img_and_data['Image'] is not None:
                self.is_loaded = True
            else:
                self.is_loaded = False
        else:
            self.is_loaded = False
