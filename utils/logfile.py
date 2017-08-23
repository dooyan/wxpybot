# -*- coding: utf-8 -*-
# 日志记录设置模块

import sys
sys.path.insert(0, "../")

import os
import logging

def console_and_logfile(logFilename):

    logdir = os.path.split(logFilename)[0]
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logform = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s'
    logging.basicConfig(
        level = logging.DEBUG,
        format = logform,
        datefmt = '%Y-%m-%d %H:%M:%S')
    formatter = logging.Formatter(logform)
    fileshandle = logging.FileHandler(logFilename)
    fileshandle.setLevel(logging.DEBUG)
    fileshandle.setFormatter(formatter)

    logging.getLogger('').addHandler(fileshandle)
    return fileshandle

if __name__ == '__main__':

    import time

    icount = 100
    console_and_logfile('../logs/testrslog')

    while icount > 0:
        icount -= 1
        logging.debug("test logging.debug")
        logging.info("test logging.info")
        logging.warning("test logging.warning")
        logging.error("test logging.error")
        logging.critical("test logging.critical")
        time.sleep(10)
