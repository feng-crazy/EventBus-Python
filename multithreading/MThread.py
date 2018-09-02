#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 19:41
# @Author  : hedengfeng
# @Site    : 
# @File    : MThread.py
# @Software: LT_controller
import asyncio
import threading
import traceback

from EventClient import EventClient
from Mlogging import MLog


class MThread(object):
    """
    我的线程框架
    """

    def __init__(self, child_class, child_class_name):
        self.run_flag = False
        self.exit_flag = False
        self._child_class = child_class
        self.recursive_lock = None
        self.event_handle_sleep = 0.0  # 单位秒
        self.thread_loop_sleep = 0.0  # 单位秒
        self.thread = threading.Thread(target=self.thread_run, args=(child_class,), name=child_class_name)
        self.thread.start()

    async def _thread_event_handle(self, event_client):
        while True:
            try:
                event_client.handle_event()
            except Exception as err:
                MLog.mlogger.warn('Exception as err:%s', err)
                MLog.mlogger.warn(traceback.format_exc())
            await asyncio.sleep(self.event_handle_sleep)  # 0秒象征协程调度

            if self.exit_flag:
                return

    async def _thread_run(self, child_thread):
        while True:
            if self.run_flag is True:
                try:
                    child_thread.thread_task()
                except Exception as err:
                    MLog.mlogger.warn('Exception as err:%s', err)
                    MLog.mlogger.warn(traceback.format_exc())
            else:
                pass
            await asyncio.sleep(self.thread_loop_sleep)

            if self.exit_flag:
                return

    def thread_run(self, child_thread):
        """
        线程函数
        :param child_thread: 子线程的实例化对象
        """
        self.recursive_lock = threading.RLock()
        event_client = EventClient()
        child_thread.setup_thread()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread_loop = asyncio.get_event_loop()
        tasks = [self._thread_event_handle(event_client), self._thread_run(child_thread)]
        future = asyncio.wait(tasks)
        thread_loop.run_until_complete(future)

        thread_loop.close()

    def start(self):
        print('start thread : ', self._child_class.thread_name)
        if self.run_flag is not True:
            self.run_flag = True

    def stop(self):
        print('stop thread : ', self._child_class.thread_name)
        if self.run_flag is True:
            self.run_flag = False

    def exit(self):
        self.exit_flag = True

    def __del__(self):
        """"""


