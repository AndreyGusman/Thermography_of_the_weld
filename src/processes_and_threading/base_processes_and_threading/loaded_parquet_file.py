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
        # self.ScrollBar_Parquet.setMaximum(self.metadata['number_frames'])

    def set_plc_data(self, plc_data):
        self.image_and_plc_data = plc_data

    def associate_img_and_plc_data(self, img_data):
        self.image_and_plc_data[f'Image {img_data["Image id"]}']['Image'] = img_data['Image']

        if img_data["Image id"] == self.metadata.get('number_frames'):
            self.is_loaded = True
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
        self.clear_data()
        self.file_name = file_name
        self.metadata = metadata.copy()
        self.image_and_plc_data = image_and_plc_data.copy()
        self.is_loaded = self.check_exist_last_image()

    def get_all_data(self):
        return self.file_name, self.metadata, self.image_and_plc_data

    def get_img_and_plc_data(self, key, select_img_id):
        if key != 'Image':
            if self.image_and_plc_data.get(key) is not None:
                read_img_and_data = self.image_and_plc_data.get(f'Image {select_img_id}').copy()
                if read_img_and_data['Image'] is not None:
                    self.screen_reference.update_arch_img(read_img_and_data)

    def check_exist_last_image(self):
        return True