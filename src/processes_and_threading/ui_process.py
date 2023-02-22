from ..interface import *
from src.config import Config
from src.processes_and_threading.base_processes_and_threading.base_process import BaseProcess
import sys
import time


class UIProcess(BaseProcess):
    def __init__(self, pipe_to_parquet, pipe_to_camera, pipe_to_main):
        super().__init__(pipe_to_main)

        # инициализация рабочего объекта
        self.app = None
        self.ui_window = None

        # временно конфиг хранится в процессе
        self.config = Config()

        # инициализация каналов связи
        self.pipe_to_main = pipe_to_main
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_camera = pipe_to_camera

        # инициализация очередей на отправку задач в соответсвующие модули
        self.queue_to_main = self.create_queue()
        self.queue_to_parquet = self.create_queue()
        self.queue_to_camera = self.create_queue()

        # инициализация очередей на выполнение задач от  соответсвующего модуля
        self.queue_from_main = self.create_queue()
        self.queue_from_parquet = self.create_queue()
        self.queue_from_camera = self.create_queue()

        # инициализация работников с каналами связи
        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.queue_from_main)
        self.to_parquet_pipe_worker = self.create_pipe_worker(self.pipe_to_parquet, self.queue_to_parquet,
                                                              self.queue_from_parquet)
        self.to_camera_pipe_worker = self.create_pipe_worker(self.pipe_to_camera, self.queue_to_camera,
                                                             self.queue_from_camera)

        # инициализация исполнителей задач с каналами связи
        self.from_main_task_executor = self.create_task_executor(self.queue_from_main, self.from_main_task_handler,
                                                                 self.default_task_handler)
        self.from_parquet_task_executor = self.create_task_executor(self.queue_from_parquet,
                                                                    self.from_parquet_task_handler,
                                                                    self.default_task_handler)
        self.from_camera_task_executor = self.create_task_executor(self.queue_from_camera,
                                                                   self.from_camera_task_handler,
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

    # метод выполняемый при старте процесса
    def run(self):
        self.action()
        self.create_logging_task('Ui working finish')

    # метод запуска потоков при закрытии главного экрана, формируется задача на останов остальных модулей
    def action(self):
        # создание потоков нельзя перенести в __init__!
        self.thread_work_with_object = self.create_thread(self.work_with_object)
        self.thread_work_with_pipe = self.create_thread(self.work_with_pipe)
        self.thread_work_with_task = self.create_thread(self.work_with_task)

        self.thread_work_with_object.start()
        self.thread_work_with_object.join()

        self.create_task_close_program(self.queue_to_main, self.queue_to_parquet, self.queue_to_camera)
        self.b_work = False

        self.create_logging_task('ui close, create task to stop program')

        self.thread_work_with_pipe.join()
        self.thread_work_with_task.join()
        # self.create_logging_task('Ui pipe worker finish')

    # задача потока работы с обьектом (создание и отслеживание действий на экране)
    def work_with_object(self):
        self.app, self.ui_window = create_ui(self)
        # self.create_logging_task(data='UI create')
        self.thread_work_with_task.start()

        self.thread_work_with_pipe.start()

        # блокирующий оператор, функция равершается при закрытии окна ui
        sys.exit(self.app.exec())

    # задача потока работы с каналами связи
    def work_with_pipe(self):
        # self.create_logging_task(data='UI pipe check')

        while self.b_work or not self.b_pipe_free:
            # возможно константы из конфига будут подтягиваться при инициализации и будут неизменными
            b_pipe_to_main_free = self.to_main_pipe_worker.work()
            b_pipe_to_camera_free = self.to_camera_pipe_worker.work()
            b_pipe_to_parquet_free = self.to_parquet_pipe_worker.work()

            self.b_pipe_free = self.check_pipe_free(b_pipe_to_main_free, b_pipe_to_camera_free, b_pipe_to_parquet_free)

    # задача потока работы с задачами
    def work_with_task(self):

        while self.b_work or not self.b_pipe_free or not self.b_queue_free:
            b_queue_from_main_free = self.from_main_task_executor.work()
            b_queue_from_camera_free = self.from_camera_task_executor.work()
            b_queue_from_parquet_free = self.from_parquet_task_executor.work()
            self.b_queue_free = self.check_pipe_free(b_queue_from_main_free, b_queue_from_camera_free,
                                                     b_queue_from_parquet_free)

    # обработчики задач
    def from_camera_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Show img':
            self.ui_window.show_img_and_plc_data(data)
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data=f'Ui process task from camera the solution is not defined, task name {name}')

    def from_main_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data=f'Ui process task from main the solution is not defined, task name {name}')

    def from_parquet_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update transfocator status':
            self.ui_window.set_status_transfocator(data)
        elif name == 'Update profibus status':
            self.ui_window.set_status_profibus(data)
        elif name == 'Metadata from parquet':
            self.ui_window.arch_win.set_metadata(data)
        elif name == 'Plc data from parquet':
            self.ui_window.arch_win.set_plc_data(data)
        elif name == 'Image from parquet file':
            self.ui_window.arch_win.associate_img_and_plc_data(data)
        elif name == 'Register parquet file':
            self.ui_window.arch_win.parquet_analyser.register_parquet_file(data)
        elif name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(data=f'Ui process task from parquet the solution is not defined, task name {name}')

    def default_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update config':
            self.config = data
        elif name == 'Start module':
            pass
        elif name == 'Stop module':
            self.b_work = False
        else:
            self.create_logging_task(data=f'Ui process default task  solution is not defined, task name {name}')

    def get_parquet_file(self, file_name):
        self.create_task(name='Request parquet file', data=file_name, queue=self.queue_to_parquet)


if __name__ == '__main__':
    pass
