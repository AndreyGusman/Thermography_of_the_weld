import time
import multiprocessing
from src.main import MainProgram

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print('start main')
    main = MainProgram()
    main.action()
    time.sleep(60)
    print('main close')