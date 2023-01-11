from ..parquet import *
from scr.processes_and_threading.base_processes_and_threading.base_process import BaseProcess


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

        # инициализация работников с каналами связи
        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.from_main_task_handler, self.default_task_handler)
        self.to_ui_pipe_worker = self.create_pipe_worker(self.pipe_to_ui, self.queue_to_ui, self.from_ui_task_handler,
                                                         self.default_task_handler)
        self.to_camera_pipe_worker = self.create_pipe_worker(self.pipe_to_camera, self.queue_to_camera,
                                                             self.from_camera_task_handler, self.default_task_handler)

        # инициализация потоков работы с каналами связи и рабочим обьектом
        self.thread_work_with_object = None
        self.thread_work_with_pipe = None

        # инициализация переменных контроля работы
        self.b_work = True
        self.b_pipe_free = False
        self.b_create_task = True

    def run(self):
        self.action()
        self.create_logging_task(data='Parquet working finish')

    def action(self):
        # создание потоков нельзя перенести в __init__!
        self.thread_work_with_object = self.create_thread(self.work_with_object)
        self.thread_work_with_pipe = self.create_thread(self.work_with_pipe)

        # запуск потоков
        self.thread_work_with_object.start()
        self.thread_work_with_pipe.start()

        self.create_logging_task(data='Parquet working create')

        # ждём пока заверщится работа
        self.thread_work_with_object.join()
        self.thread_work_with_pipe.join()

    # задача потока работы с каналами связи
    def work_with_pipe(self):
        # работа c Pipe пока есть разрешение на работу или каналы не свободны
        while self.b_work or not self.b_pipe_free:
            b_pipe_to_main_free = self.to_main_pipe_worker.work(timeout=self.parquet_worker.config.PIPE_TIMEOUT,
                                                                received_limit=self.parquet_worker.config.TRY_SEND_RECEIVE_LIMIT)
            b_pipe_to_ui_free = self.to_ui_pipe_worker.work(timeout=self.parquet_worker.config.PIPE_TIMEOUT,
                                                            received_limit=self.parquet_worker.config.TRY_SEND_RECEIVE_LIMIT)
            b_pipe_to_camera_free = self.to_camera_pipe_worker.work(timeout=self.parquet_worker.config.PIPE_TIMEOUT,
                                                                    received_limit=self.parquet_worker.config.TRY_SEND_RECEIVE_LIMIT)

            self.b_pipe_free = self.check_pipe_free(b_pipe_to_main_free, b_pipe_to_ui_free, b_pipe_to_camera_free)

    def work_with_object(self):
        # пока задач не создаёт, только исполняет
        pass

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
        else:
            self.create_logging_task(data=f'Parquet process default task  solution is not defined, task name {name}')


if __name__ == "__main__":
    pass
