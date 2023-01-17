import threading


class BaseThread(threading.Thread):
    """
    Базовый класс потока программы. Для более удобной конфигурации переопределяет методы запуска потока из
    родительского класса threading.Thread.
        Args: work - целевая функция потока

    """

    def __init__(self, work):
        threading.Thread.__init__(self)
        self.work = work

    def run(self):
        """
        Метод запуска потока obj.start(). После запуска выполняет целевую функцию action().
        :return: None
        """
        self.action()

    def action(self):
        """
        Задача потока. Выполняет переданную при инициализации функцию work().
        :return: None
        """
        self.work()


if __name__ == '__main__':
    pass
