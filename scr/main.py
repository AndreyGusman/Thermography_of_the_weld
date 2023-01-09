from processes import *
import multiprocessing


def main():
    work = True

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

    while work:
        if p_main_btw_ui.poll(timeout=0.1):
            task = p_main_btw_ui.recv()
            if task.name == 'Write Log':
                print(task.data)
            else:
                pass

        if p_main_btw_parquet.poll(timeout=0.1):
            task = p_main_btw_parquet.recv()
            if task.name == 'Write Log':
                print(task.data)
            else:
                pass
        if p_main_btw_camera.poll(timeout=0.1):
            task = p_main_btw_camera.recv()
            if task.name == 'Write Log':
                print(task.data)
            else:
                pass

    camera_and_nn_process.join()
    ui_process.join()
    parquet_process.join()


if __name__ == '__main__':
    main()
