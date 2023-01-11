# TODO прописать класс базового потока, потока работы с Pipe, потока создателя задач

import threading


class BaseThread(threading.Thread):
    def __init__(self, work):
        threading.Thread.__init__(self)
        self.work = work

    def run(self):
        self.action()

    def action(self):
        self.work()
