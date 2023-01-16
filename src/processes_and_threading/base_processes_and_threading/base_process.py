import multiprocessing
from src.processes_and_threading.base_processes_and_threading.base_task import Task
from src.processes_and_threading.base_processes_and_threading.pipe_worker import PipeWorker
from src.processes_and_threading.base_processes_and_threading.base_thread import BaseThread


class BaseProcess(multiprocessing.Process):
    """
    Базовый класс процесса программы. Для более удобной конфигурации переопределяет методы запуска процесса из
    родительского класса multiprocessing.Process.
        Args: pipe_to_main - объект multiprocessing.connection.Connection до главного модуля программы
        Attributes: task - ссылка на объект Task (шаблон задачи, для обмена информацией между модулями программы)

    """

    def __init__(self, pipe_to_main):
        multiprocessing.Process.__init__(self)
        self.pipe_to_main = pipe_to_main
        self.task = Task

    def run(self):
        """
        Метод запуска процесс obj.start()
        :return: None
        """
        pass

    def action(self):
        """
        Задача процесса
        :return: None
        """
        pass

    def create_task(self, name, data, queue):
        """
        Метод создания задачи и перемещения задачи в очередь на отправку
        Args:name - имя задачи
             data - данные задачи
             queue - очередь на отправку
        :return: None
        """
        task = self.task(name, data)
        task.write_init_data()
        queue.put(task)

    @staticmethod
    def decode_task(task: Task):
        """
        Метод распаковки задачи
        Args: task - входящая задача
        :return:name - имя задачи
             data - данные задачи
             task - экземпляр задачи с заполненными данными об исполнителе
        """
        name, data = task.get_data()
        task.write_execution_data()
        return name, data, task

    def create_logging_task(self, data):
        """
        Метод создания логируещего сообщения. Данное сообщение будет отправлено в обход очереди на отправку
        Args: data - текст лога
        :return: None
        """
        task = self.task('Write Log', data)
        task.write_init_data()
        self.pipe_to_main.send(task)

    def create_task_close_program(self, queue1, queue2, queue3):
        """
        Метод формирования команды на завершение работы модулей
        Args: queue1-3 - очереди на отправку сообщений в соответсвующие модули
        :return: None
        """
        task = self.task('Stop module', False)
        queue1.put(task)
        queue2.put(task)
        queue3.put(task)

    @staticmethod
    def logging_processing(task: Task):
        """
        Метод позволяющий перехватить поток вывода в консоль и отобразить сообщение лога в дочернем процессе
        Args: task - экземпляр задачи
        :return: Вывод в консоль
        """
        print(task.data)

    @staticmethod
    def create_pipe_worker(pipe_connection, queue_task, task_handler, default_task_handler):
        """
        Метод создающий рабочего с объектом multiprocessing.connection.Connection
        Args:pipe_connection - объект multiprocessing.connection.Connection
             queue_task - объект очереди на отправку задач
             task_handler - ссылка на функцию обработки задач от соответсвующего модуля программы
             default_task_handler  - ссылка на функцию обработки стандартных задач
        :return: экземпляр класса PipeWorker
        """
        return PipeWorker(pipe_connection, queue_task, task_handler, default_task_handler)

    @staticmethod
    def create_queue():
        """
        Метод создание объекта очереди multiprocessing.Queue()
        Args:
        :return: экземпляр класса multiprocessing.Queue()
        """
        return multiprocessing.Queue()

    @staticmethod
    def check_pipe_free(cond_pipe_1, cond_pipe_2, cond_pipe_3):
        """
        Метод проверки свободы каналов связи
        Args:cond_pipe_1-3 - состояние канала связи
        :return: True - если все каналы свободны
                 False - если хотя бы один канал занят
        """
        if cond_pipe_1 and cond_pipe_2 and cond_pipe_3:
            return True
        else:
            return False

    @staticmethod
    def create_thread(work):
        """
        Метод создаёт базовый поток
        Args: work - целевая функция потока
        :return: объект экземпляра класса BaseThread() с целевой функцией work
        """
        return BaseThread(work)
