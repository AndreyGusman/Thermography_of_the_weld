import time
from src.config import Config


class PipeWorker:
    """
    Базовый класс работы с объектом multiprocessing.connection.Connection. Реализует методы работы с очередью
    multiprocessing.Queue, считывание входящих задач и отправку созданных задач в соответствующий модуль.
        Args: pipe_connection - канал связи до модуля, экземпляр класса multiprocessing.connection.Connection;
              queue_for_sending - очередь на отправку задач, экземпляр класс multiprocessing.Queue;
              queue_for_execution - очередь на выполнение задач, экземпляр класс multiprocessing.Queue.
        Attributes: timeout - время прослушивания канала связи
                    send_recv_time_limit - лимит времени в секундах! после которого канал считается свободным
                    time_last_recv - время последнего приёма задачи
                    time_last_send - время последнего отправьения задачи
    """

    def __init__(self, pipe_connection, queue_for_sending, queue_for_execution):
        self.pipe_connection = pipe_connection
        self.queue_for_sending = queue_for_sending
        self.queue_for_execution = queue_for_execution

        self.timeout = Config.PIPE_TIMEOUT
        self.send_recv_time_limit = Config.SEND_RECEIVE_TIME_LIMIT

        self.time_last_recv = time.time()
        self.time_last_send = time.time()

    def work(self):
        """
        Метод обработки канала связи. Слушаем канал в течении времени  timeout, если есть входящие задачи считываем и
        отправляем в очередь на выполнение задач и обновляем время последнего получения.
        Далее смотрим есть ли в очереди задачи на отправку, если есть то считываем задачу с очереди и отправляем в
        соответствующий канал и обновляем время последнего отправления.
        Args:
        :return: результат метода self.watch_received_limit()(см. описание метода)
        """
        if self.pipe_connection.poll(timeout=self.timeout):
            recv_task = self.pipe_connection.recv()
            self.queue_for_execution.put(recv_task)
            self.time_last_recv = time.time()

        if not self.queue_for_sending.empty():
            send_task = self.queue_for_sending.get()
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


if __name__ == '__main__':
    pass
