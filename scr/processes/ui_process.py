from ..interface import *
import threading
from scr.processes.base_process import BaseProcess
import sys


class UIProcess(BaseProcess):
    def __init__(self, pipe_to_parquet, pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)
        self.t2 = None
        self.t1 = None
        self.ui = None
        self.app = None
        self.MainWindow = None
        self.pipe_to_main = pipe_to_main
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_camera = pipe_to_camera

    def run(self):
        self.create_threading()

    def create_threading(self):
        self.t1 = threading.Thread(target=self.thread_1_task)
        self.t2 = threading.Thread(target=self.thread_2_task)

        self.t1.start()

        self.t1.join()

        self.t2.join()

    def thread_1_task(self):
        self.ui, self.app, self.MainWindow = UiMainWindow.create_ui()
        self.MainWindow.show()
        self.t2.start()

        sys.exit(self.app.exec_())

    def thread_2_task(self):
        while True:
            if self.pipe_to_camera.poll(timeout=0.1):
                task = self.pipe_to_camera.recv()
                task.write_execution_data()
                name, data = task.get_data()
                if name == 'Show img':
                    UiMainWindow.update_current_img(data[0], self.ui, self.MainWindow, False)
                    UiMainWindow.update_broke_img(data[1], self.ui, self.MainWindow, True)
            else:
                pass
