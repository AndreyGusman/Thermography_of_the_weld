from src.processes_and_threading import CameraAndNNProcess, ParquetProcess, UIProcess
from src.processes_and_threading.base_processes_and_threading.base_process import BaseProcess
import multiprocessing
from src.config import Config


# класс наследуется от базового класса, чтобы иметь нативную поддержку работы с Pipe и Task
class MainProgram(BaseProcess):
    def __init__(self):
        super().__init__(None)
        # собственный экземпляр конфигурации

        self.config = Config()

        # объявление  процессов
        self.parquet_process = None
        self.ui_process = None
        self.camera_and_nn_process = None

        # объявление каналов связи
        self.p_camera_btw_main = None
        self.p_main_btw_camera = None
        self.p_parquet_btw_main = None
        self.p_ui_btw_main = None
        self.p_main_btw_parquet = None
        self.p_ui_btw_parquet = None
        self.p_main_btw_ui = None
        self.p_parquet_btw_ui = None
        self.p_parquet_btw_camera = None
        self.p_camera_btw_parquet = None
        self.p_ui_btw_camera = None
        self.p_camera_btw_ui = None

        # инициализация очередей на отправку задач в соответсвующие модули
        self.queue_to_camera = BaseProcess.create_queue()
        self.queue_to_parquet = BaseProcess.create_queue()
        self.queue_to_ui = BaseProcess.create_queue()

        # инициализация очередей на выполнение задач от  соответсвующего модуля
        self.queue_from_camera = BaseProcess.create_queue()
        self.queue_from_parquet = BaseProcess.create_queue()
        self.queue_from_ui = BaseProcess.create_queue()

        # инициализация работников с каналами связи
        self.to_ui_pipe_worker = None
        self.to_parquet_pipe_worker = None
        self.to_camera_pipe_worker = None

        # инициализация исполнителей задач с каналами связи
        self.from_ui_task_executor = None
        self.from_parquet_task_executor = None
        self.from_camera_task_executor = None

        # инициализация потоков работы с каналами связи и рабочим обьектом
        self.thread_work_with_object = None
        self.thread_work_with_pipe = None
        self.thread_work_with_task = None

        # инициализация переменных контроля работы
        self.b_work = True
        self.b_pipe_free = False
        self.b_queue_free = False
        self.b_create_task = True
        self.b_work_camera_process = False
        self.b_work_ui_process = False
        self.b_work_parquet_process = False

    def init_pipes(self):
        # инициализация двунаправленных каналов связи
        self.p_camera_btw_ui, self.p_ui_btw_camera = multiprocessing.Pipe(duplex=True)
        self.p_camera_btw_parquet, self.p_parquet_btw_camera = multiprocessing.Pipe(duplex=True)
        self.p_parquet_btw_ui, self.p_ui_btw_parquet = multiprocessing.Pipe(duplex=True)
        self.p_main_btw_ui, self.p_ui_btw_main = multiprocessing.Pipe(duplex=True)
        self.p_main_btw_parquet, self.p_parquet_btw_main = multiprocessing.Pipe(duplex=True)
        self.p_main_btw_camera, self.p_camera_btw_main = multiprocessing.Pipe(duplex=True)

    def init_processes(self):
        # инициализация процессов
        self.camera_and_nn_process = CameraAndNNProcess(self.p_camera_btw_ui, self.p_camera_btw_parquet,
                                                        self.p_camera_btw_main)
        self.ui_process = UIProcess(self.p_ui_btw_parquet, self.p_ui_btw_camera, self.p_ui_btw_main)
        self.parquet_process = ParquetProcess(self.p_parquet_btw_ui, self.p_parquet_btw_camera, self.p_parquet_btw_main)

    def start_processes(self):

        # запуск процессов
        self.ui_process.start()
        self.camera_and_nn_process.start()
        self.parquet_process.start()

    def init_pipe_worker(self):
        # инициализация работников с каналами связи
        self.to_camera_pipe_worker = BaseProcess.create_pipe_worker(self.p_main_btw_camera, self.queue_to_camera,
                                                                    self.queue_from_camera)
        self.to_parquet_pipe_worker = BaseProcess.create_pipe_worker(self.p_main_btw_parquet, self.queue_to_parquet,
                                                                     self.queue_from_parquet)
        self.to_ui_pipe_worker = BaseProcess.create_pipe_worker(self.p_main_btw_ui, self.queue_to_ui,
                                                                self.queue_from_ui)

    def init_task_executor(self):
        # инициализация исполнителей задач с каналами связи
        self.from_camera_task_executor = BaseProcess.create_task_executor(self.queue_from_camera,
                                                                          self.from_camera_task_handler,
                                                                          self.default_task_handler)
        self.from_parquet_task_executor = BaseProcess.create_task_executor(self.queue_from_parquet,
                                                                           self.from_parquet_task_handler,
                                                                           self.default_task_handler)
        self.from_ui_task_executor = BaseProcess.create_task_executor(self.queue_from_ui, self.from_ui_task_handler,
                                                                      self.default_task_handler)
        # расширяем список стандартных задач для главного процесса
        self.from_camera_task_executor.default_task_name.append('Write Log')
        self.from_parquet_task_executor.default_task_name.append('Write Log')
        self.from_ui_task_executor.default_task_name.append('Write Log')

    def run(self):
        pass

    def action(self):
        self.init_pipes()
        self.init_processes()
        self.start_processes()
        self.init_pipe_worker()
        self.init_task_executor()

        # создание потоков нельзя перенести в __init__!
        self.thread_work_with_object = BaseProcess.create_thread(self.work_with_object)
        self.thread_work_with_pipe = BaseProcess.create_thread(self.work_with_pipe)
        self.thread_work_with_task = BaseProcess.create_thread(self.work_with_task)
        # запуск потоков, обработчик Pipe запускается из work_with_object
        self.thread_work_with_object.start()
        self.thread_work_with_pipe.start()
        self.thread_work_with_task.start()
        # ждём пока заверщится работа
        self.thread_work_with_object.join()
        self.thread_work_with_pipe.join()
        self.thread_work_with_task.join()

        self.camera_and_nn_process.join()
        print('Camera close')

        self.ui_process.join()
        print('Ui close')

        self.parquet_process.join()
        print('Parquet close')

    def work_with_pipe(self):
        # работа c Pipe пока есть разрешение на работу или каналы не свободны
        while self.b_work or not self.b_pipe_free:
            b_pipe_to_camera_free = self.to_camera_pipe_worker.work()
            b_pipe_to_ui_free = self.to_ui_pipe_worker.work()
            b_pipe_to_parquet_free = self.to_parquet_pipe_worker.work()
            self.b_pipe_free = BaseProcess.check_pipe_free(b_pipe_to_camera_free, b_pipe_to_ui_free,
                                                           b_pipe_to_parquet_free)

    def work_with_object(self):
        while self.b_create_task:
            self.b_work_camera_process = self.camera_and_nn_process.is_alive()
            self.b_work_ui_process = self.ui_process.is_alive()
            self.b_work_parquet_process = self.parquet_process.is_alive()
            self.b_create_task = self.b_work_camera_process or self.b_work_ui_process or self.b_work_parquet_process
            if not self.b_work:
                print(self.b_work_camera_process, self.b_work_ui_process, self.b_work_parquet_process)
        print('Main object worker finish')

        # задача потока работы с задачами

    def work_with_task(self):
        while self.b_work or not self.b_pipe_free or not self.b_queue_free:
            b_queue_from_camera_free = self.from_camera_task_executor.work()
            b_queue_from_ui_free = self.from_ui_task_executor.work()
            b_queue_from_parquet_free = self.from_parquet_task_executor.work()
            self.b_queue_free = BaseProcess.check_pipe_free(b_queue_from_camera_free, b_queue_from_ui_free,
                                                            b_queue_from_parquet_free)

    # обработчики задач
    def from_ui_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            pass

    def from_parquet_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            pass

    def from_camera_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'next task':
            pass
        elif name == 'next task':
            pass
        else:
            pass

    def default_task_handler(self, task):
        name, data, decode_task = self.decode_task(task)
        if name == 'Update config':
            self.config = data
        elif name == 'Start module':
            pass
        elif name == 'Stop module':
            self.b_work = False
        elif name == 'Write Log':
            print(task.data)
        else:
            print(f'Main not the solution is not defined, task name {name}')


def main():
    main_prog = MainProgram()
    main_prog.action()
    print('main close')


if __name__ == '__main__':
    main()
