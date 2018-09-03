#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 11:20
# @Author  : hedengfeng
# @Site    : 
# @File    : Mlogging.py
# @Software: LT_controller

import logging
from logging.handlers import TimedRotatingFileHandler
import sys


LOG_FILE = 'M.log'


class MLog(object):
    """
        日志功能类
    """
    mlogger = logging.getLogger('MLogging')
    mlogger.setLevel(logging.DEBUG)
    log_fmt = '%(asctime)s,%(thread)s:%(filename)s:%(lineno)d :%(message)s'
    formatter = logging.Formatter(log_fmt)

    # create a handler,use to write log file
    log_file_handler = TimedRotatingFileHandler(LOG_FILE, when='D', interval=1, backupCount=7)
    log_file_handler.setLevel(logging.WARN)

    # define format
    log_file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # add file handler
    mlogger.addHandler(log_file_handler)
    mlogger.addHandler(console_handler)


if __name__ == '__main__':
    MLog.mlogger.debug('debug message,%d,%s', 2, 'sb')
    MLog.mlogger.info('info message')
