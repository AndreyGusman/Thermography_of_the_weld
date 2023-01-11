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
