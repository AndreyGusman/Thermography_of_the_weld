import multiprocessing
from scr.processes.task import Task
from scr.config import Config


class BaseProcess(multiprocessing.Process):
    def __init__(self, pipe_to_main):
        multiprocessing.Process.__init__(self)
        self.pipe_to_main = pipe_to_main
        self.task = Task
        self.config = Config()

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

    def create_task_close_program(self, con1, con2, con3):
        task = self.task('Close program', False)
        con1.send(task)
        con2.send(task)
        con3.send(task)

    @staticmethod
    def logging_processing(task: Task):
        print(task.data)

    @staticmethod
    def create_pipe_worker(pipe_connection, queue_task, task_handler):
        return PipeWorker(pipe_connection, queue_task, task_handler)

    @staticmethod
    def create_queue():
        return multiprocessing.Queue()


class PipeWorker:
    def __init__(self, pipe_connection, queue_task, task_handler):
        self.pipe_connection = pipe_connection
        self.queue_task = queue_task
        self.task_handler = task_handler

    def work(self, timeout):
        if self.pipe_connection.poll(timeout=timeout):
            recv_task = self.pipe_connection.recv()
            self.task_handler(recv_task)
        if not self.queue_task.empty():
            send_task = self.queue_task.get()
            self.pipe_connection.send(send_task)
