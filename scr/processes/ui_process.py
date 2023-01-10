from ..interface import *
from scr.config import Config
import threading
from scr.processes.base_process import BaseProcess
import sys


class UIProcess(BaseProcess):
    def __init__(self, pipe_to_parquet, pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)
        self.ui = None
        self.app = None
        self.MainWindow = None
        self.config = Config()

        self.pipe_to_main = pipe_to_main
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_camera = pipe_to_camera

        self.queue_to_main = self.create_queue()
        self.queue_to_parquet = self.create_queue()
        self.queue_to_camera = self.create_queue()

        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.from_main_task_handler)
        self.to_parquet_pipe_worker = self.create_pipe_worker(self.pipe_to_parquet, self.queue_to_parquet,
                                                              self.from_parquet_task_handler)
        self.to_camera_pipe_worker = self.create_pipe_worker(self.pipe_to_camera, self.queue_to_camera,
                                                             self.from_camera_task_handler)

        self.t1 = None
        self.t2 = None
        self.b_work = True

    def run(self):
        self.create_threading()

    def create_threading(self):
        self.t1 = threading.Thread(target=self.thread_1_task)
        self.t2 = threading.Thread(target=self.thread_2_task)

        self.t1.start()
        self.t1.join()
        self.b_work = False
        self.create_logging_task('ui close, create task to stop program')

        self.create_task_close_program(self.pipe_to_main, self.pipe_to_parquet, self.pipe_to_camera)

        self.t2.join()

    def thread_1_task(self):
        self.ui, self.app, self.MainWindow = UiMainWindow.create_ui()
        self.MainWindow.show()
        self.t2.start()
        self.create_logging_task(data='UI create')
        sys.exit(self.app.exec_())

    def thread_2_task(self):
        self.create_logging_task(data='UI pipe check')
        while self.b_work:
            self.to_main_pipe_worker.work(timeout=self.config.PIPE_TIMEOUT)
            self.to_camera_pipe_worker.work(timeout=self.config.PIPE_TIMEOUT)
            self.to_parquet_pipe_worker.work(timeout=self.config.PIPE_TIMEOUT)

    def from_camera_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Show img':
            UiMainWindow.update_current_img(data[0], self.ui, self.MainWindow, False)
            UiMainWindow.update_broke_img(data[1], self.ui, self.MainWindow, True)
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
