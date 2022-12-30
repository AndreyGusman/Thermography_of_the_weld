import multiprocessing

from scr.processes.task import Task


class BaseProcess(multiprocessing.Process):
    def __init__(self, pipe_to_main):
        multiprocessing.Process.__init__(self)
        self.pipe_to_main = pipe_to_main
        self.task = Task

    def run(self):
        pass

    def action(self):
        pass

    def create_task(self, name, data, connect):
        task = self.task(name, data)
        task.write_init_data()
        connect.send(task)

    @staticmethod
    def task_decoder(task: Task):
        name, data = task.get_data()
        task.write_execution_data()
        return name, data, task

    def create_logging_task(self, data):
        task = self.task('Write Log', data)
        task.write_init_data()
        self.pipe_to_main.send(task)
