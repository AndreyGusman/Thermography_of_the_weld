import time
import random as rd
from ..parquet import *
from src.processes_and_threading.base_processes_and_threading.base_process import BaseProcess


class ParquetProcess(BaseProcess):
    def __init__(self, pipe_to_ui, pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)

        # инициализация рабочего объекта
        self.parquet_worker = ParquetWorker()

        # инициализация каналов связи
        self.pipe_to_main = pipe_to_main
        self.pipe_to_ui = pipe_to_ui
        self.pipe_to_camera = pipe_to_camera

        # инициализация очередей на отправку задач в соответсвующие модули
        self.queue_to_main = self.create_queue()
        self.queue_to_ui = self.create_queue()
        self.queue_to_camera = self.create_queue()

        # инициализация очередей на выполнение задач от  соответсвующего модуля
        self.queue_from_main = self.create_queue()
        self.queue_from_camera = self.create_queue()
        self.queue_from_ui = self.create_queue()

        # инициализация работников с каналами связи
        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.queue_from_main)
        self.to_ui_pipe_worker = self.create_pipe_worker(self.pipe_to_ui, self.queue_to_ui, self.queue_from_ui)
        self.to_camera_pipe_worker = self.create_pipe_worker(self.pipe_to_camera, self.queue_to_camera,
                                                             self.queue_from_camera)

        # инициализация исполнителей задач с каналами связи
        self.from_main_task_executor = self.create_task_executor(self.queue_from_main, self.from_main_task_handler,
                                                                 self.default_task_handler)
        self.from_camera_task_executor = self.create_task_executor(self.queue_from_camera,
                                                                   self.from_camera_task_handler,
                                                                   self.default_task_handler)
        self.from_ui_task_executor = self.create_task_executor(self.queue_from_ui, self.from_ui_task_handler,
                                                               self.default_task_handler)

        # инициализация потоков работы с каналами связи и рабочим обьектом
        self.thread_work_with_object = None
        self.thread_work_with_pipe = None
        self.thread_work_with_task = None

        # инициализация переменных контроля работы
        self.b_work = True
        self.b_pipe_free = False
        self.b_queue_free = False
        self.b_create_task = True
        # Временные переменные
        self.profibus_status = False
        self.transfocator_status = False

    def run(self):
        self.action()
        self.create_logging_task(data='Parquet working finish')

    def action(self):
        # создание потоков нельзя перенести в __init__!
        self.thread_work_with_object = self.create_thread(self.work_with_object)
        self.thread_work_with_pipe = self.create_thread(self.work_with_pipe)
        self.thread_work_with_task = self.create_thread(self.work_with_task)
        # запуск потоков
        self.thread_work_with_object.start()
        self.thread_work_with_pipe.start()
        self.thread_work_with_task.start()

        self.create_logging_task(data='Parquet working create')

        # ждём пока заверщится работа
        self.thread_work_with_object.join()
        self.create_logging_task(data='Parquet work with obj finish')
        self.thread_work_with_pipe.join()
        self.create_logging_task(data='Parquet work with pipe finish')
        self.thread_work_with_task.join()
        self.create_logging_task(data='Parquet work with task finish')

    # задача потока работы с каналами связи
    def work_with_pipe(self):
        # работа c Pipe пока есть разрешение на работу или каналы не свободны
        while self.b_work or not self.b_pipe_free:
            b_pipe_to_main_free = self.to_main_pipe_worker.work()
            b_pipe_to_ui_free = self.to_ui_pipe_worker.work()
            b_pipe_to_camera_free = self.to_camera_pipe_worker.work()

            self.b_pipe_free = self.check_pipe_free(b_pipe_to_main_free, b_pipe_to_ui_free, b_pipe_to_camera_free)

    def work_with_object(self):
        self.create_task(name='Update transfocator status', data=self.transfocator_status, queue=self.queue_to_ui)
        self.create_task(name='Update profibus status', data=self.profibus_status, queue=self.queue_to_ui)
        # пока нет оборудования применяются функции затычки
        timer_change_net_status = time.time()
        timer_change_tech_info = time.time()
        while self.b_create_task:
            if time.time() - timer_change_net_status > 2:
                timer_change_net_status = time.time()
                if rd.random() > 0.5:
                    self.profibus_status = not self.profibus_status
                    self.create_task(name='Update profibus status', data=self.profibus_status, queue=self.queue_to_ui)

                if rd.random() > 0.5:
                    self.transfocator_status = not self.transfocator_status
                    self.create_task(name='Update transfocator status', data=self.transfocator_status,
                                     queue=self.queue_to_ui)

            if time.time() - timer_change_tech_info > 2:
                timer_change_tech_info = time.time()


    # задача потока работы с задачами
    def work_with_task(self):
        while self.b_work or not self.b_pipe_free or not self.b_queue_free:
            b_queue_from_main_free = self.from_main_task_executor.work()
            b_queue_from_ui_free = self.from_ui_task_executor.work()
            b_queue_from_parquet_free = self.from_camera_task_executor.work()
            self.b_queue_free = self.check_pipe_free(b_queue_from_main_free, b_queue_from_ui_free,
                                                     b_queue_from_parquet_free)

    # обработчики задач
    def from_main_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Parquet process task from main the solution is not defined, task name {name}')

    def from_ui_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data=f'Parquet process task from ui the solution is not defined, task name {name}')

    def from_camera_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Write to parquet':
            answer = self.parquet_worker.write_to_parquet_from_list(data, self.parquet_worker.config.TITTLE)
            if answer is not None:
                self.create_logging_task(data=answer)
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Parquet process task from camera the solution is not defined, task name {name}')

    def default_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update config':
            self.parquet_worker.config = data
        elif name == 'Start module':
            pass
        elif name == 'Stop module':
            self.b_work = False
            self.b_create_task = False
        else:
            self.create_logging_task(data=f'Parquet process default task  solution is not defined, task name {name}')


if __name__ == "__main__":
    pass
