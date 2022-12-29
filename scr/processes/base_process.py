import multiprocessing


class BaseProcess(multiprocessing.Process):
    def __init__(self, pipe_to_main):
        multiprocessing.Process.__init__(self)
        self.pipe_to_main = pipe_to_main
        self.task =

    def run(self):
        pass

    def action(self):
        pass
