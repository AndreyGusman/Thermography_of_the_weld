import time
from config import Config


class PipeWorker:
    """
    Базовый класс работы с объектом multiprocessing.connection.Connection. Реализует методы работы с очередью
    multiprocessing.Queue(), перехват общих для всех процессов задач и вызов соответствующего обработчика задач.
        Args: pipe_connection - канал связи до модуля, экземпляр класса multiprocessing.connection.Connection;
              queue_task - очередь на отправку задач, экземпляр класс multiprocessing.Queue;
              task_handler - ссылка на обработчик задач от соответстующего модуля;
              default_task_handler - ссылка на обработчик стандартных задач.
        Attributes: default_task_name - список наименований стандартных задач
                    timeout - время прослушивания канала связи
                    send_recv_time_limit - лимит времени в секундах! после которого канал считается свободным
                    time_last_recv - время последнего приёма задачи
                    time_last_send - время последнего отправьения задачи
    """
    default_task_name = ['Update config', 'Start module', 'Stop module']

    def __init__(self, pipe_connection, queue_task, task_handler, default_task_handler):
        self.pipe_connection = pipe_connection
        self.queue_task = queue_task
        self.task_handler = task_handler
        self.default_task_handler = default_task_handler

        self.timeout = Config.PIPE_TIMEOUT
        self.send_recv_time_limit = Config.SEND_RECEIVE_TIME_LIMIT

        self.time_last_recv = time.time()
        self.time_last_send = time.time()

    def work(self):
        """
        Метод обработки канала связи. Слушаем канал в течении времени  timeout, если есть входящие задачи считываем и
        проверяем наименование задачи. Если задача находится в списке стандартных вызывается обработчик стадндартных
        задач, иначе вызывает обработчик задач от модуля, указанный при инициализации. в любом случае обновляем время
        последнего получения задачи.
        Далее смотрим есть ли в очереди задачи на отправку, если есть то считываем задачу с очереди и отправляем в
        соответствующий канал и обновляем время последнего отправления.
        Args:
        :return: результат метода self.watch_received_limit()(см. описание метода)
        """
        if self.pipe_connection.poll(timeout=self.timeout):
            recv_task = self.pipe_connection.recv()
            if recv_task.name in self.default_task_name:
                self.default_task_handler(recv_task)
            else:
                self.task_handler(recv_task)
            self.time_last_recv = time.time()

        if not self.queue_task.empty():
            send_task = self.queue_task.get()
            self.pipe_connection.send(send_task)
            self.time_last_send = time.time()

        return self.watch_received_limit()

    def watch_received_limit(self):
        """
         Метод проверяющий свободен ли канал связи или занят
         Сравнивает время последней отправки и приёма сообщения с текущим временем системы
         Args:
         :return: True - если в течении времени self.send_recv_time_limit не осуществлялось приёма или передачи задач
                  False - если в течении времени self.send_recv_time_limit осуществляллся приём или передачи задач
         """
        if time.time() - self.time_last_recv > self.send_recv_time_limit \
                and time.time() - self.time_last_send > self.send_recv_time_limit:
            return True
        else:
            return False
