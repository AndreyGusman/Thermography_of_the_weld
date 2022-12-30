from ..camera import Camera
import scr.config as config
from scr.processes.base_process import BaseProcess
import time
import random


class CameraAndNNProcess(BaseProcess):
    def __init__(self, pipe_to_ui, pipe_to_parquet, pipe_to_main):
        super().__init__(pipe_to_main)
        self.camera = Camera()
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_ui = pipe_to_ui

    def run(self):
        self.create_cup()
        self.create_logging_task(data='Camera capture establish')
        while not config.PROGRAM_CAMERA_CLOSE:
            list_img = self.get_img_from_camera()
            self.create_task(name='Show img', data=list_img, connect=self.pipe_to_ui)
            self.create_task(name='Write to parquet', data=self.create_task_to_write_parquet(list_img),
                             connect=self.pipe_to_parquet)
        self.camera.capture.release()
        self.create_logging_task(data='Camera capture closed')

    def create_cup(self):
        self.camera.get_capture()

    def get_img_from_camera(self):
        ret_img = []
        img = self.camera.get_img()
        orig_img = self.camera.get_origin_img()
        ret_img.append(orig_img)
        ret_img.append(img)
        return ret_img

    def create_task_to_write_parquet(self, img_list):
        img_to_parquet = list.copy(img_list)
        img_to_parquet[0] = self.camera.convert_img_to_one_row(img_to_parquet[0])
        img_to_parquet[1] = self.camera.convert_img_to_one_row(img_to_parquet[1])
        value = [time.time(), random.randint(10, 10000), random.random(),
                 config.OUT_FRAME_WIDTH * config.OUT_FRAME_HEIGHT, list(img_to_parquet[0]), list(img_to_parquet[1])]
        return value


if __name__ == "__main__":
    pass
