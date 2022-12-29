from processes import *
import multiprocessing


def main():
    q_img_camera_to_ui = multiprocessing.Queue()
    q_img_camera_to_parquet = multiprocessing.Queue()
    camera_and_nn_process = CameraAndNNProcess(q_img_camera_to_ui,q_img_camera_to_parquet)
    ui_process = UIProcess(q_img_camera_to_ui)
    parquet_process = ParquetProcess(q_img_camera_to_parquet)

    camera_and_nn_process.start()
    ui_process.start()
    parquet_process.start()

    camera_and_nn_process.join()
    ui_process.join()
    parquet_process.join()


if __name__ == '__main__':
    main()
