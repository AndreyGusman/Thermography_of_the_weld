from src.config import Config
import time


class TaskExecutor:
    """
    Базовый класс работы с объектом multiprocessing.Queue. Реализует методы работы с очередью
    multiprocessing.Queue, считывание входящих задач и их выполнение.
        Args: queue_for_execution - очередь на выполнение задач, экземпляр класс multiprocessing.Queue;
              task_handler - ссылка на обработчик задач от соответстующего модуля;
              default_task_handler - ссылка на обработчик стандартных задач.
        Attributes: default_task_name - список наименований стандартных задач
                    timeout - время прослушивания канала связи
                    send_recv_time_limit - лимит времени в секундах! после которого обработчик считается свободным
                    time_last_recv - время последнего приёма задачи
    """
    default_task_name = ['Update config', 'Start module', 'Stop module']

    def __init__(self, queue_for_execution, task_handler, default_task_handler):
        self.queue_for_execution = queue_for_execution
        self.task_handler = task_handler
        self.default_task_handler = default_task_handler

        self.send_recv_time_limit = Config.SEND_RECEIVE_TIME_LIMIT
        self.timeout = Config.TASK_EXECUTOR_TIMEOUT

        self.time_last_recv = time.time()

    def work(self):
        """
        Метод обработки очереди задач на выполнение.Смотрим очередь на выполнение, если есть входящие задачи то
        считываем её с очереди. Если задача находится в списке стандартных вызывается обработчик стадндартных
        задач, иначе вызывает обработчик задач от модуля, указанный при инициализации. в любом случае обновляем время
        последнего получения задачи.
        time.sleep(self.timeout) необходима для уменьшения колличества вызовов фунции и уменьшения нагрузки на процессор
        Args:
        :return: результат метода self.watch_received_limit()(см. описание метода)
        """
        time.sleep(self.timeout)
        if not self.queue_for_execution.empty():
            recv_task = self.queue_for_execution.get()
            if recv_task.name in self.default_task_name:
                self.default_task_handler(recv_task)
            else:
                self.task_handler(recv_task)
        return self.watch_received_limit()

    def watch_received_limit(self):
        """
         Метод проверяющий свободен ли канал связи или занят
         Сравнивает время последней отправки и приёма сообщения с текущим временем системы
         Args:
         :return: True - если в течении времени self.send_recv_time_limit не осуществлялось приёма задач
                  False - если в течении времени self.send_recv_time_limit осуществлялся приём задач
         """
        if time.time() - self.time_last_recv > self.send_recv_time_limit:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
