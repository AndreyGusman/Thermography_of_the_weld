import time
import multiprocessing
from src.main import MainProgram
import cgitb

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("Version from 2023 01 18 v .01")
    print('start main')

    cgitb.enable(format='text')
    main = MainProgram()
    main.action()
    print('main close')
