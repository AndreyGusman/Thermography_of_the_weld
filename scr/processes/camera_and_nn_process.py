from ..camera import Camera
from scr.processes.base_process import BaseProcess
import time
import random


class CameraAndNNProcess(BaseProcess):
    def __init__(self, pipe_to_ui, pipe_to_parquet, pipe_to_main):
        super().__init__(pipe_to_main)
        self.camera = Camera()

        self.pipe_to_main = pipe_to_main
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_ui = pipe_to_ui

        self.queue_to_main = self.create_queue()
        self.queue_to_parquet = self.create_queue()
        self.queue_to_ui = self.create_queue()

        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.from_main_task_handler)
        self.to_parquet_pipe_worker = self.create_pipe_worker(self.pipe_to_parquet, self.queue_to_parquet,
                                                              self.from_parquet_task_handler)
        self.to_ui_pipe_worker = self.create_pipe_worker(self.pipe_to_ui, self.queue_to_ui,
                                                         self.from_ui_task_handler)

        self.b_work = True

    def run(self):
        self.action()

    def action(self):
        self.create_cup()
        self.create_logging_task(data='Camera and NN working create')

        while self.b_work:
            list_img = self.get_img_from_camera()

            self.create_task(name='Show img', data=list_img, queue=self.queue_to_ui)
            self.create_task(name='Write to parquet', data=self.create_task_to_write_parquet(list_img),
                             queue=self.queue_to_parquet)

            self.to_main_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT)
            self.to_ui_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT)
            self.to_parquet_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT)

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
        data_frame = [time.time(), random.randint(10, 10000), random.random(),
                      self.camera.config.OUT_FRAME_WIDTH * self.camera.config.OUT_FRAME_HEIGHT, list(img_to_parquet[0]),
                      list(img_to_parquet[1])]
        return data_frame

    def from_ui_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data='Camera and NN process task from ui the solution is not defined')

    def from_main_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data='Camera and NN process task from main the solution is not defined')

    def from_parquet_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data='Camera and NN process task from parquet the solution is not defined')


if __name__ == "__main__":
    pass
