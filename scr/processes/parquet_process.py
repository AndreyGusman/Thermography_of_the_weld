from ..parquet import *
import threading
import multiprocessing
import time
import sys
import scr.config as config


class ParquetProcess(multiprocessing.Process):
    def __init__(self, queue_to_write_parquet):
        multiprocessing.Process.__init__(self)
        self.queue_to_write_parquet = queue_to_write_parquet
        self.parquet_worker = ParquetWorker()

    def run(self):
        self.action()

    def action(self):
        time.sleep(5)
        while config.PROGRAM_FINISH:
            if self.queue_to_write_parquet.empty():
                pass
            else:
                data_to_write = self.queue_to_write_parquet.get()
                self.parquet_worker.write_to_parquet_from_list(data_to_write, config.TITTLE)
