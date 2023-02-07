class ParquetViewer:
    def __init__(self, hmi_reference):
        self.metadata = None
        self.image_and_plc_data = None
        self.hmi_reference = hmi_reference

    def associate_img_and_plc_data(self, img_data):
        self.image_and_plc_data[f'Image {img_data["Image id"]}']['Image'] = img_data['Image']
        self.hmi_reference.update_arch_img(self.image_and_plc_data[f'Image {img_data["Image id"]}'])

    def set_metadata(self, metadata):
        self.metadata = metadata

    def set_plc_data(self, plc_data):
        self.image_and_plc_data = plc_data
