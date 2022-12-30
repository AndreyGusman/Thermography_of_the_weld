from processes import *
import multiprocessing


def main():
    p_camera_btw_ui, p_ui_btw_camera = multiprocessing.Pipe(duplex=True)
    p_camera_btw_parquet, p_parquet_btw_camera = multiprocessing.Pipe(duplex=True)
    p_parquet_btw_ui, p_ui_btw_parquet = multiprocessing.Pipe(duplex=True)
    p_main_btw_ui, p_ui_btw_main = multiprocessing.Pipe(duplex=True)
    p_main_btw_parquet, p_parquet_btw_main = multiprocessing.Pipe(duplex=True)
    p_main_btw_camera, p_camera_btw_main = multiprocessing.Pipe(duplex=True)

    camera_and_nn_process = CameraAndNNProcess(p_camera_btw_ui, p_camera_btw_parquet, p_camera_btw_main)
    ui_process = UIProcess(p_ui_btw_parquet, p_ui_btw_camera, p_ui_btw_main)
    parquet_process = ParquetProcess(p_parquet_btw_ui, p_parquet_btw_camera, p_parquet_btw_main)

    camera_and_nn_process.start()
    ui_process.start()
    parquet_process.start()

    camera_and_nn_process.join()
    ui_process.join()
    parquet_process.join()


if __name__ == '__main__':
    main()
