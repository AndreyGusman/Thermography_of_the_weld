from ..parquet import *
from scr.processes.base_process import BaseProcess


class ParquetProcess(BaseProcess):
    def __init__(self, pipe_to_ui, pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)
        self.parquet_worker = ParquetWorker()
        self.pipe_to_main = pipe_to_main
        self.pipe_to_ui = pipe_to_ui
        self.pipe_to_camera = pipe_to_camera

    def run(self):
        self.action()

    def action(self):
        self.create_logging_task(data='parquet working create')

        while True:
            if self.pipe_to_camera.poll(timeout=0.1):
                task = self.pipe_to_camera.recv()
                name, data, _ = self.decode_task(task)
                if name == 'Write to parquet':
                    answer = self.parquet_worker.write_to_parquet_from_list(data, self.parquet_worker.config.TITTLE)
                    if answer is not None:
                        self.create_logging_task(data=answer)
            else:
                pass
