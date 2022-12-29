from ..camera import *
import multiprocessing
import scr.config as config
import time
import random


class CameraAndNNProcess(multiprocessing.Process):
    def __init__(self, queue_to_show_img, queue_to_write_parquet):
        multiprocessing.Process.__init__(self)
        self.camera_cup = Camera()
        self.queue_to_show_img = queue_to_show_img
        self.queue_to_write_parquet = queue_to_write_parquet

    def run(self):
        self.create_cup()
        while config.PROGRAM_FINISH:
            print(config.PROGRAM_FINISH)
            list_img = self.get_img_from_camera()
            self.create_task_to_show_img(list_img, self.queue_to_show_img)
            self.create_task_to_write_parquet(list_img, self.queue_to_write_parquet)

    def create_cup(self):
        self.camera_cup.get_capture()

    def get_img_from_camera(self):
        ret_img = []
        img = self.camera_cup.get_img()
        orig_img = self.camera_cup.get_origin_img()
        ret_img.append(orig_img)
        ret_img.append(img)

        return ret_img

    @staticmethod
    def check_overflow_queue(queue, queue_name):
        if queue.qsize() > config.MAX_QUEUE_SIZE:
            print(f'The size of {queue_name} is {queue.qsize()}')

    def create_task_to_show_img(self, img_list, queue):
        queue.put(img_list)
        self.check_overflow_queue(queue, 'queue_to_show_img')

    def create_task_to_write_parquet(self, img_list, queue):
        img_to_parquet = list.copy(img_list)
        img_to_parquet[0] = self.camera_cup.convert_img_to_one_row(img_to_parquet[0])
        img_to_parquet[1] = self.camera_cup.convert_img_to_one_row(img_to_parquet[1])
        value = []
        value.append(time.time())
        value.append(random.randint(10, 10000))
        value.append(random.random())
        value.append(config.OUT_FRAME_WIDTH * config.OUT_FRAME_HEIGHT)
        value.append(list(img_to_parquet[0]))
        value.append(list(img_to_parquet[1]))
        queue.put(value)
        self.check_overflow_queue(queue, 'queue_to_write_parquet')


if __name__ == "__main__":
    pass
