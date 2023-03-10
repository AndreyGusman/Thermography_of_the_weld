from ..camera import Camera
from src.processes_and_threading.base_processes_and_threading.base_process import BaseProcess
from src.data_format import DataFormat

import random


class CameraAndNNProcess(BaseProcess):
    def __init__(self, pipe_to_ui, pipe_to_parquet, pipe_to_main, shared_array):
        super().__init__(pipe_to_main, shared_array)

        # инициализация рабочего объекта
        self.camera = Camera()

        # инициализация каналов связи
        self.pipe_to_main = pipe_to_main
        self.pipe_to_parquet = pipe_to_parquet
        self.pipe_to_ui = pipe_to_ui

        # инициализация очередей на отправку задач в соответсвующие модули
        self.queue_to_main = self.create_queue()
        self.queue_to_parquet = self.create_queue()
        self.queue_to_ui = self.create_queue()

        # инициализация очередей на выполнение задач от  соответсвующего модуля
        self.queue_from_main = self.create_queue()
        self.queue_from_parquet = self.create_queue()
        self.queue_from_ui = self.create_queue()

        # инициализация работников с каналами связи
        self.to_main_pipe_worker = self.create_pipe_worker(self.pipe_to_main, self.queue_to_main,
                                                           self.queue_from_main)
        self.to_parquet_pipe_worker = self.create_pipe_worker(self.pipe_to_parquet, self.queue_to_parquet,
                                                              self.queue_from_parquet)
        self.to_ui_pipe_worker = self.create_pipe_worker(self.pipe_to_ui, self.queue_to_ui,
                                                         self.queue_from_ui)

        # инициализация исполнителей задач с каналами связи
        self.from_main_task_executor = self.create_task_executor(self.queue_from_main, self.from_main_task_handler,
                                                                 self.default_task_handler)
        self.from_parquet_task_executor = self.create_task_executor(self.queue_from_parquet,
                                                                    self.from_parquet_task_handler,
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
        self.b_force_stop = False

    # метод выполняемый при старте процесса
    def run(self):
        self.action()
        self.create_logging_task(data='Camera and NN working finish')

    # метод запуска потоков
    def action(self):
        # создание потоков нельзя перенести в __init__!
        self.thread_work_with_object = self.create_thread(self.work_with_object)
        self.thread_work_with_pipe = self.create_thread(self.work_with_pipe)
        self.thread_work_with_task = self.create_thread(self.work_with_task)

        # запуск потоков
        self.thread_work_with_object.start()
        self.thread_work_with_pipe.start()
        self.thread_work_with_task.start()

        # ждём пока заверщится работа
        self.thread_work_with_object.join()
        self.thread_work_with_pipe.join()
        self.thread_work_with_task.join()

    # задача потока работы с каналами связи
    def work_with_pipe(self):
        # работа c Pipe пока есть разрешение на работу или каналы не свободны
        while (self.b_work or not self.b_pipe_free) and not self.b_force_stop:
            b_pipe_to_main_free = self.to_main_pipe_worker.work()
            b_pipe_to_ui_free = self.to_ui_pipe_worker.work()
            b_pipe_to_parquet_free = self.to_parquet_pipe_worker.work()
            self.b_pipe_free = self.check_pipe_free(b_pipe_to_main_free, b_pipe_to_ui_free, b_pipe_to_parquet_free)

    # задача потока работы с объектом
    def work_with_object(self):
        # захватываем изображение с камеры
        self.camera.get_capture()
        # self.create_logging_task(data='Camera capture create')
        # пока есть разрешение считываем кадр с камеры и создаём задачи
        while (self.b_create_task and self.camera.is_open) and not self.b_force_stop:
            dict_img = self.get_img_from_camera()
            self.create_task(name='Show img', data=dict_img, queue=self.queue_to_ui)
            self.create_task(name='Write to parquet', data=self.camera.create_data_frame_to_parquet(),
                             queue=self.queue_to_parquet)

        # self.create_logging_task(data='Camera stopped')
        # освобождаем камеру
        try:
            self.camera.capture.release()
        except:
            pass
        self.create_logging_task(data='Camera capture closed')

    # задача потока работы с задачами
    def work_with_task(self):
        while (self.b_work or not self.b_pipe_free or not self.b_queue_free) and not self.b_force_stop:
            b_queue_from_main_free = self.from_main_task_executor.work()
            b_queue_from_ui_free = self.from_ui_task_executor.work()
            b_queue_from_parquet_free = self.from_parquet_task_executor.work()
            self.b_queue_free = self.check_pipe_free(b_queue_from_main_free, b_queue_from_ui_free,
                                                     b_queue_from_parquet_free)

    def get_img_from_camera(self):
        ret_dict = DataFormat.dict_camera_to_interface.copy()
        ret_dict['current_img'] = self.camera.get_current_img_and_plc_data()
        if random.random() > 0.95:
            ret_dict['broken_img'] = self.camera.test_get_broken_img_and_plc_data(ret_dict['current_img'].get('image'))
        return ret_dict

    def create_task_to_write_parquet(self):
        data_frame = self.camera.create_data_frame_to_parquet()
        return data_frame

    # обработчики задач
    def from_ui_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Camera and NN process task from ui the solution is not defined, task name {name}')

    def from_main_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Camera and NN process task from main the solution is not defined, task name {name}')

    def from_parquet_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update plc data':
            self.camera.update_current_plc_data(data)
        elif name == 'next task':
            pass
        else:
            self.create_logging_task(
                data=f'Camera and NN process task from parquet the solution is not defined, task name {name}')

    def default_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update config':
            self.camera.config = data
        elif name == 'Start module':
            pass
        elif name == 'Stop module':
            self.b_create_task = False
            self.b_work = False
            self.b_force_stop = True
        else:
            self.create_logging_task(data=f'Camera process default task  solution is not defined, task name {name}')


if __name__ == "__main__":
    pass
