from ..interface import *
import threading
import multiprocessing
import time
import sys
import scr.config as config


class UIProcess(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.t2 = None
        self.t1 = None
        self.ui = None
        self.app = None
        self.MainWindow = None
        self.queue = queue

    def run(self):
        self.create_threading()

    def create_threading(self):
        self.t1 = threading.Thread(target=self.thread_1_task)
        self.t2 = threading.Thread(target=self.thread_2_task)

        self.t1.start()

        self.t1.join()
        print('thread 1 finish')
        config.PROGRAM_FINISH = False
        self.t2.join()

        print('thread 2 finish')

    def thread_1_task(self):
        self.ui, self.app, self.MainWindow = UiMainWindow.create_ui()
        self.MainWindow.show()
        self.t2.start()

        sys.exit(self.app.exec_())

    def thread_2_task(self):
        while config.PROGRAM_FINISH:
            if self.queue.empty():
                pass
            else:

                list_img = self.queue.get()
                UiMainWindow.update_current_img(list_img[0], self.ui, self.MainWindow, False)
                UiMainWindow.update_broke_img(list_img[1], self.ui, self.MainWindow, True)
