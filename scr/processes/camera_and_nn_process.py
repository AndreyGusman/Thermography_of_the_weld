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
                                                           self.from_main_task_handler, self.default_task_handler)
        self.to_parquet_pipe_worker = self.create_pipe_worker(self.pipe_to_parquet, self.queue_to_parquet,
                                                              self.from_parquet_task_handler, self.default_task_handler)
        self.to_ui_pipe_worker = self.create_pipe_worker(self.pipe_to_ui, self.queue_to_ui,
                                                         self.from_ui_task_handler, self.default_task_handler)

        self.b_create_task = True
        self.b_work = True
        self.b_pipe_free = False

    def run(self):
        self.action()
        self.create_logging_task(data='Camera and NN working finish')

    def action(self):
        self.create_cup()
        self.create_logging_task(data='Camera and NN working create')

        while self.b_work or not self.b_pipe_free:
            if self.b_create_task:
                list_img = self.get_img_from_camera()
                self.create_task(name='Show img', data=list_img, queue=self.queue_to_ui)
                self.create_task(name='Write to parquet', data=self.create_task_to_write_parquet(list_img),
                                 queue=self.queue_to_parquet)

            b_pipe_to_main_free = self.to_main_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT,
                                                                received_limit=self.camera.config.TRY_SEND_RECEIVE_LIMIT)
            b_pipe_to_ui_free = self.to_ui_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT,
                                                            received_limit=self.camera.config.TRY_SEND_RECEIVE_LIMIT)
            b_pipe_to_parquet_free = self.to_parquet_pipe_worker.work(timeout=self.camera.config.PIPE_TIMEOUT,
                                                                      received_limit=self.camera.config.TRY_SEND_RECEIVE_LIMIT)
            self.b_pipe_free = self.check_pipe_free(b_pipe_to_main_free, b_pipe_to_ui_free, b_pipe_to_parquet_free)

        self.camera.capture.release()
        self.create_logging_task(data='Camera capture closed')

    def create_cup(self):
        self.camera.get_capture()

    def get_img_from_camera(self):
        ret_img = []
        img = self.camera.get_img()
        color_img = self.camera.color_img_to_the_colormap(img)
        ret_img.append(img)
        ret_img.append(color_img)
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
            self.create_logging_task(
                data=f'Camera and NN process task from ui the solution is not defined, task name {name}')

    def from_main_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Camera and NN process task from main the solution is not defined, task name {name}')

    def from_parquet_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Camera and NN process task from parquet the solution is not defined, task name {name}')

    def default_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update config':
            self.camera.config = data
        elif name == 'Start module':
            pass
        elif name == 'Stop module':
            self.b_create_task = False
            self.b_work = False
        else:
            self.create_logging_task(data=f'Camera process default task  solution is not defined, task name {name}')


if __name__ == "__main__":
    pass
