import multiprocessing
from src.processes_and_threading.base_processes_and_threading.base_task import Task
from src.processes_and_threading.base_processes_and_threading.pipe_worker import PipeWorker
from src.processes_and_threading.base_processes_and_threading.base_thread import BaseThread


class BaseProcess(multiprocessing.Process):
    def __init__(self, pipe_to_main):
        multiprocessing.Process.__init__(self)
        self.pipe_to_main = pipe_to_main
        self.task = Task

    def run(self):
        pass

    def action(self):
        pass

    def create_task(self, name, data, queue):
        task = self.task(name, data)
        task.write_init_data()
        queue.put(task)

    @staticmethod
    def decode_task(task: Task):
        name, data = task.get_data()
        task.write_execution_data()
        return name, data, task

    def create_logging_task(self, data):
        task = self.task('Write Log', data)
        task.write_init_data()
        self.pipe_to_main.send(task)

    def create_task_close_program(self, queue1, queue2, queue3):
        task = self.task('Stop module', False)
        queue1.put(task)
        queue2.put(task)
        queue3.put(task)

    @staticmethod
    def logging_processing(task: Task):
        print(task.data)

    @staticmethod
    def create_pipe_worker(pipe_connection, queue_task, task_handler, default_task_handler):
        return PipeWorker(pipe_connection, queue_task, task_handler, default_task_handler)

    @staticmethod
    def create_queue():
        return multiprocessing.Queue()

    @staticmethod
    def check_pipe_free(cond_pipe_1, cond_pipe_2, cond_pipe_3):
        if cond_pipe_1 and cond_pipe_2 and cond_pipe_3:
            return True
        else:
            return False

    @staticmethod
    def create_thread(work):
        return BaseThread(work)
