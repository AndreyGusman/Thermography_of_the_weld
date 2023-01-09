from processes import *
import multiprocessing
from scr.config import Config


class MainProgram:
    def __init__(self):
        self.config = Config()
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

        while self.b_work:
            if p_main_btw_ui.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_ui.recv()
                if task.name == 'Write Log':
                    print(task.data)
                else:
                    pass

            if p_main_btw_parquet.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_parquet.recv()
                if task.name == 'Write Log':
                    print(task.data)
                else:
                    pass
            if p_main_btw_camera.poll(timeout=self.config.PIPE_TIMEOUT):
                task = p_main_btw_camera.recv()
                if task.name == 'Write Log':
                    print(task.data)
                else:
                    pass

        camera_and_nn_process.join()
        ui_process.join()
        parquet_process.join()


if __name__ == '__main__':
    main = MainProgram()
    main.main()
