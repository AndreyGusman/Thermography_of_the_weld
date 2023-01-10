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


class PipeWorker:
    default_task_name = ['Update config', 'Start module', 'Stop module']

    def __init__(self, pipe_connection, queue_task, task_handler, default_task_handler):
        self.pipe_connection = pipe_connection
        self.queue_task = queue_task
        self.task_handler = task_handler
        self.default_task_handler = default_task_handler
        self.count_recv = 0
        self.count_send = 0

    def work(self, timeout, received_limit):
        if self.pipe_connection.poll(timeout=timeout):
            recv_task = self.pipe_connection.recv()
            if recv_task.name in self.default_task_name:
                self.default_task_handler(recv_task)
            else:
                self.task_handler(recv_task)

            self.count_recv = 0
        elif self.count_recv < received_limit * 2:
            self.count_recv += 1

        if not self.queue_task.empty():
            send_task = self.queue_task.get()
            self.pipe_connection.send(send_task)

            self.count_send = 0
        elif self.count_send < received_limit * 2:
            self.count_send += 1

        return self.watch_received_limit(received_limit=received_limit)

    def watch_received_limit(self, received_limit):
        if self.count_recv > received_limit and self.count_send > received_limit:
            return True
        else:
            return False
