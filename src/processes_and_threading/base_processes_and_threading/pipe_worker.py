import time
from config import Config


class PipeWorker:
    default_task_name = ['Update config', 'Start module', 'Stop module']

    def __init__(self, pipe_connection, queue_task, task_handler, default_task_handler):
        self.pipe_connection = pipe_connection
        self.queue_task = queue_task
        self.task_handler = task_handler
        self.default_task_handler = default_task_handler

        self.timeout = Config.PIPE_TIMEOUT
        self.send_recv_time_limit = Config.SEND_RECEIVE_TIME_LIMIT

        self.time_last_recv = time.time()
        self.time_last_send = time.time()

    def work(self):
        if self.pipe_connection.poll(timeout=self.timeout):
            recv_task = self.pipe_connection.recv()
            if recv_task.name in self.default_task_name:
                self.default_task_handler(recv_task)
            else:
                self.task_handler(recv_task)
            self.time_last_recv = time.time()

        if not self.queue_task.empty():
            send_task = self.queue_task.get()
            self.pipe_connection.send(send_task)
            self.time_last_send = time.time()

        return self.watch_received_limit()

    def watch_received_limit(self):
        if time.time() - self.time_last_recv > self.send_recv_time_limit \
                and time.time() - self.time_last_send > self.send_recv_time_limit:
            return True
        else:
            return False
