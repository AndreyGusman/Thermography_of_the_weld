import multiprocessing
import threading
import time


class Task:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.process_creater = None
        self.thread_creater = None
        self.creation_time = None
        self.process_executor = None
        self.thread_executor = None
        self.execution_time = None
        self.exception = None
        self.result = None

    def write_init_data(self):
        self.process_creater = multiprocessing.current_process().name
        self.thread_creater = threading.current_thread().name
        self.creation_time = time.time()

    def write_execution_data(self):
        self.process_executor = multiprocessing.current_process().name
        self.thread_executor = threading.current_thread().name
        self.execution_time = time.time()

    def set_positive_result(self):
        self.result = True

    def set_negative_result(self):
        self.result = False

    def get_data(self):
        return self.name, self.data

