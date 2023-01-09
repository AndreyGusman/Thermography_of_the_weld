from ..parquet import *
from scr.processes.base_process import BaseProcess


class ParquetProcess(BaseProcess):
    def __init__(self, pipe_to_ui,pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)
        self.parquet_worker = ParquetWorker()
        self.pipe_to_main = pipe_to_main
        self.pipe_to_ui = pipe_to_ui
        self.pipe_to_camera = pipe_to_camera

    def run(self):
        self.action()

    def action(self):

        while True:
            if self.pipe_to_camera.poll(timeout=1):
                task = self.pipe_to_camera.recv()
                task.write_execution_data()
                name, data = task.get_data()
                if name == 'Write to parquet':
                    self.parquet_worker.write_to_parquet_from_list(data, self.parquet_worker.config.TITTLE)
            else:
                pass
