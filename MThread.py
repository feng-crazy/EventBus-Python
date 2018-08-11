#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 19:41
# @Author  : hedengfeng
# @Site    : 
# @File    : MThread.py
# @Software: LT_controller

import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler

from eventbus.MsgClient import MsgClient
from eventbus.MsgTarget import MsgTarget


class MThread(object):
    """
    我的线程框架
    """

    def __init__(self, child_class, child_class_name):
        self.run_flag = False
        self._child_class = child_class
        self.thread = threading.Thread(target=self.thread_run, args=(child_class,), name=child_class_name)
        self.thread.start()

    def thread_run(self, child_thread):
        """
        线程函数
        :param child_thread: 子线程的实例化对象
        """
        msg_client = MsgClient()

        #  0.1秒处理一次eventBus队列里面的消息
        scheduler = BackgroundScheduler()
        scheduler.add_job(msg_client.handle_event, 'interval', seconds=0.1, args=())
        scheduler.start()

        child_thread.setup_thread()
        while True:
            # msg_client.handle_event()
            if self.run_flag is True:
                child_thread.thread_task()
            else:
                pass
            # time.sleep(0.5)

    def start(self):
        print('start thread : ', self._child_class.thread_name)
        if self.run_flag is not True:
            self.run_flag = True

    def stop(self):
        print('stop thread : ', self._child_class.thread_name)
        if self.run_flag is True:
            self.run_flag = False

    def __del__(self):
        """"""


