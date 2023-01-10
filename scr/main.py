from processes_and_threading import *
import multiprocessing
from scr.config import Config

# TODO переработать цикл работы с Pipe под шаблон базового класса
class MainProgram:
    def __init__(self):
        self.config = Config()
        self.b_work_camera_process = False
        self.b_work_ui_process = False
        self.b_work_parquet_process = False
        self.b_work = True

    def main(self):
        p_camera_btw_ui, p_ui_btw_camera = multiprocessing.Pipe(duplex=True)
        p_camera_btw_parquet, p_parquet_btw_camera = multiprocessing.Pipe(duplex=True)
        p_parquet_btw_ui, p_ui_btw_parquet = multiprocessing.Pipe(duplex=True)
        p_main_btw_ui, p_ui_btw_main = multiprocessing.Pipe(duplex=True)
        p_main_btw_parquet, p_parquet_btw_main = multiprocessing.Pipe(duplex=True)
        p_main_btw_camera, p_camera_btw_main = multiprocessing.Pipe(duplex=True)

        camera_and_nn_process = CameraAndNNProcess(p_camera_btw_ui, p_camera_btw_parquet, p_camera_btw_main)
        ui_process = UIProcess(p_ui_btw_parquet, p_ui_btw_camera, p_ui_btw_main)
        parquet_process = ParquetProcess(p_parquet_btw_ui, p_parquet_btw_camera, p_parquet_btw_main)

        ui_process.start()
        camera_and_nn_process.start()
        parquet_process.start()

        while self.b_work or self.b_work_camera_process or self.b_work_ui_process or self.b_work_parquet_process:
            if p_main_btw_ui.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_ui.recv()
                if task.name == 'Write Log':
                    print(task.data)
                elif task.name == 'Stop module':
                    self.b_work = False
                elif task.name == 'Next task':
                    pass
                else:
                    print(f'Main process task from ui, the solution is not defined, task name ')

            if p_main_btw_parquet.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_parquet.recv()
                if task.name == 'Write Log':
                    print(task.data)
                elif task.name == 'Next task':
                    pass
                else:
                    print(f'Main process task from parquet, the solution is not defined, task name ')

            if p_main_btw_camera.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_camera.recv()
                if task.name == 'Write Log':
                    print(task.data)
                elif task.name == 'Next task':
                    pass
                else:
                    print(f'Main process task from camera, the solution is not defined, task name ')

            self.b_work_camera_process = camera_and_nn_process.is_alive()
            self.b_work_ui_process = ui_process.is_alive()
            self.b_work_parquet_process = parquet_process.is_alive()

        camera_and_nn_process.join()
        print('camera close')
        ui_process.join()
        print('ui close')
        parquet_process.join()
        print('parquet close')


if __name__ == '__main__':
    main = MainProgram()
    main.main()
    print('main close')
