import multiprocessing
import threading
import time


class Task:
    """
    Базовый класс описывающий шаблон задачи и методы работы с задачей. Экземпляры данного класса используются для обмена
    сообщениями между процессами программы.
        Args: name - наименование задачи
              data - данные необходимые для исполнения задачи
        Attributes: process_creater - процесс создатель задачи
        thread_creater - поток создатель задачи
        creation_time - время создания задачи
        process_executor - процесс исполнитель задачи
        thread_executor - процесс исполнитель задачи
        execution_time - время распаковки/исполнения задачи
        exception - возникшее исключение при выполнение задачи
        result -  результат выполнение False/True

    """

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.process_creater = None
        self.thread_creater = None
        self.creation_time = None
        self.process_executor = None
        self.thread_executor = None
        self.execution_time = None
        self.exception = None
        self.result = None

    def write_init_data(self):
        """
        Метод фиксации данных при создании задачи
        :return: None
        """
        self.process_creater = multiprocessing.current_process().name
        self.thread_creater = threading.current_thread().name
        self.creation_time = time.time()

    def write_execution_data(self):
        """
        Метод фиксации данных при выполнении задачи
        :return: None
        """
        self.process_executor = multiprocessing.current_process().name
        self.thread_executor = threading.current_thread().name
        self.execution_time = time.time()

    def set_positive_result(self):
        """
        Метод вызываемый при успешном выполнении задачи, устанавливает соответствующий аттрибут в True
        :return: None
        """
        self.result = True

    def set_negative_result(self):
        """
        Метод вызываемый при появлении исключения в ходе выполнения задачи, устанавливает соответствующий аттрибут в False
        :return: None
        """
        self.result = False

    def get_data(self):
        """
        Метод позволяющий получить наименование и данные задачи
        :return: name - наименование задачи
                 data - данные задачи
        """
        return self.name, self.data


if __name__ == '__main__':
    pass
