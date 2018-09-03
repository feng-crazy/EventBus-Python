#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 18:31
# @Author  : hedengfeng
# @Site    : 
# @File    : test_eventbus.py
# @Software: LT_controller
import asyncio
import os
import signal
import threading
import time
import traceback

from EventBus import EventBus
from EventClient import EventClient
from MThread import MThread
from EventTarget import EventTarget
from EventType import EventType
from Mlogging import MLog


class TestEventTarget1(EventTarget):
    """
    test EventTarget
    """
    def __init__(self):
        super(TestEventTarget1, self).__init__(self)
        self.subscribe(EventType.EVENT_SYSTEM_TIME_1, self)
        self.subscribe(EventType.EVENT_TEST_THREAD_2, self)
        self.subscribe(EventType.EVENT_TEST_TARGET_2, self)
        
    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        # print('TestEventTarget1 ', 'event_handle', event, event_content)
        if event == EventType.EVENT_SYSTEM_TIME_1:
            print('TestEventTarget1 ..每一秒定时处理')
        elif event == EventType.EVENT_TEST_TARGET_2:
            print('TestEventTarget1.. 收到 target2的事件')
        elif event == EventType.EVENT_TEST_THREAD_2:
            pass

    def exec(self):
        """
            publish_event
        """
        event = EventType.EVENT_TEST_TARGET_1
        event_content = (str(time.time())).encode()
        # print('TestEventTarget1 publish_event:', event, event_content)
        # self.publish_event(event, event_content)
        
    def __del__(self):
        self.unsubscribe(EventType.EVENT_SYSTEM_TIME_1, self)
        self.unsubscribe(EventType.EVENT_TEST_THREAD_2, self)
        self.unsubscribe(EventType.EVENT_TEST_TARGET_2, self)
        super(TestEventTarget1, self).__del__()


class TestEventTarget2(EventTarget):
    """
    test EventTarget
    """

    def __init__(self):
        super(TestEventTarget2, self).__init__(self)
        self.subscribe(EventType.EVENT_SYSTEM_TIME_1, self)
        self.subscribe(EventType.EVENT_TEST_THREAD_1, self)
        self.subscribe(EventType.EVENT_TEST_TARGET_1, self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        # print('TestEventTarget2 ', 'event_handle', event, event_content)
        if event == EventType.EVENT_SYSTEM_TIME_1:
            print('TestEventTarget2 ..每一秒定时处理')
        elif event == EventType.EVENT_TEST_TARGET_1:
            print('TestEventTarget2.. 收到 target1的事件')
        elif event == EventType.EVENT_TEST_THREAD_1:
            pass

    def exec(self):
        """
            publish_event
        """
        event = EventType.EVENT_TEST_TARGET_2
        event_content = (str(time.time())).encode()
        # self.publish_event(event, event_content)
        # print('TestEventTarget2 publish_event:', event, event_content)

    def __del__(self):
        self.unsubscribe(EventType.EVENT_SYSTEM_TIME_1, self)
        self.unsubscribe(EventType.EVENT_TEST_THREAD_1, self)
        self.unsubscribe(EventType.EVENT_TEST_TARGET_1, self)
        super(TestEventTarget2, self).__del__()


class TestThread1(MThread, EventTarget):
    """
    test
    """
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.test_target1 = None
        # 该类构造父类位置很重要
        MThread.__init__(self, self, thread_name)

    def thread_task(self):
        """
        线程主循环函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        event = EventType.EVENT_TEST_THREAD_1
        event_content = (str(time.time())).encode()
        # print('TestThread1 publish_event:', event, event_content)
        # self.publish_event(event, event_content)
        self.test_target1.exec()

    def setup_thread(self):
        """
        子线程初始操作函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        EventTarget.__init__(self, self)  # 该父类的构造必须是要再该线程执行中，最开始执行
        self.event_handle_sleep = 0.1  # 单位秒
        self.thread_loop_sleep = 2  # 单位秒
        print('setup_thread...........', threading.current_thread(), self.thread_name)
        self.test_target1 = TestEventTarget1()
        self.subscribe(EventType.EVENT_SYSTEM_STARTUP, self)
        self.subscribe(EventType.EVENT_TEST_THREAD_2, self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        # print('TestThread1 ' 'event_handle', event, event_content)
        if event == EventType.EVENT_SYSTEM_STARTUP:
            self.start()
            print('TestThread1 .. 系统启动事件')
        elif event == EventType.EVENT_TEST_THREAD_2:
            print('TestThread1.. 收到 thread2的事件')

    def __del__(self):
        self.unsubscribe(EventType.EVENT_SYSTEM_STARTUP, self)
        self.unsubscribe(EventType.EVENT_TEST_THREAD_2, self)
        super(TestThread1, self).__del__()


class TestThread2(MThread, EventTarget):
    """
    test
    """
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.test_target2 = None
        # 该类构造父类必须要最后
        MThread.__init__(self, self, thread_name)

    def thread_task(self):
        """
        线程主循环函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        event = EventType.EVENT_TEST_THREAD_2
        event_content = (str(time.time())).encode()
        # print('TestThread2 publish_event:', event, event_content)
        # self.publish_event(event, event_content)
        self.test_target2.exec()
        # print('TestThread2..............................time.sleep(2)')

    def setup_thread(self):
        """
        子线程初始操作函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        EventTarget.__init__(self, self)  # 该父类的构造必须是要再该线程执行中，最开始执行

        self.event_handle_sleep = 0.1  # 单位秒
        self.thread_loop_sleep = 2  # 单位秒
        print('setup_thread...........', threading.current_thread(), self.thread_name)
        self.test_target2 = TestEventTarget2()
        self.subscribe(EventType.EVENT_SYSTEM_STARTUP, self)
        self.subscribe(EventType.EVENT_TEST_THREAD_1, self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        # print('TestThread2 ', 'event_handle', event, event_content)
        if event == EventType.EVENT_SYSTEM_STARTUP:
            self.start()
            print('TestThread2 .. 系统启动事件')
        elif event == EventType.EVENT_TEST_THREAD_1:
            print('TestThread2.. 收到 thread1的事件')

    def __del__(self):
        self.unsubscribe(EventType.EVENT_SYSTEM_STARTUP, self)
        self.unsubscribe(EventType.EVENT_TEST_THREAD_1, self)
        super(TestThread2, self).__del__()


class TestSendEvent(MThread, EventTarget):
    """
    test
    """
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.test_target2 = None
        # 该类构造父类必须要最后
        MThread.__init__(self, self, thread_name)

    def thread_task(self):
        """
        线程主循环函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        data = input('please input test event>:')
        event = data
        event_content = b''
        self.publish_event(event, event_content)

    def setup_thread(self):
        """
        子线程初始操作函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        EventTarget.__init__(self, self)  # 该父类的构造必须是要再该线程执行中，最开始执行
        self.event_handle_sleep = 3  # 单位秒
        self.thread_loop_sleep = 2  # 单位秒
        print('setup_thread...........', threading.current_thread(), self.thread_name)

    def __del__(self):
        super(TestSendEvent, self).__del__()


class MainThread(object):
    def __init__(self):
        self.test_input_mthread = None
        self.thread_1 = None
        self.thread_2 = None
        self.eventbus = EventBus()
        self.main_event_client = EventClient()

        self.main_thread_exit_flag = False

        main_loop = asyncio.get_event_loop()
        tasks = [self.system_initialize(), self.main_task_handle(),
                 self.system_timer(), self.delay_system_startup()]
        future = asyncio.wait(tasks)
        main_loop.run_until_complete(future)

        main_loop.close()

    async def system_timer(self):
        """
        发布系统的每一秒的定时事件
        """
        old_time = time.time()
        while True:
            current_time = time.time()
            time_diff = current_time - old_time
            if time_diff >= 1.0:
                # event = EventType.EVENT_SYSTEM_TIME_1
                # event_content = bytes()
                # self.main_event_client.publish_event(event, event_content)
                old_time = current_time

            await asyncio.sleep(0.01)

            if self.main_thread_exit_flag:
                break
        return

    async def main_task_handle(self):
        """
        主线程的消息客户端事件处理
        """
        # print('main_task_handle: ', threading.get_ident())
        while True:
            if self.main_event_client is not None:
                try:
                    self.main_event_client.handle_event()
                except Exception as err:
                    MLog.mlogger.warn('Exception as err:%s', err)
                    MLog.mlogger.warn(traceback.format_exc())
            await asyncio.sleep(0.01)

            if self.main_thread_exit_flag:
                break
        return

    async def system_initialize(self):
        self.test_input_mthread = TestSendEvent('test send event thread')
        self.test_input_mthread.start()
        self.thread_1 = TestThread1('thread_1')
        # self.thread_1.start()

        self.thread_2 = TestThread2('thread_1')
        # self.thread_2.start()

        # 初始化完成之后循环处理广播
        while True:
            try:
                time.sleep(1)
            except Exception as err:
                MLog.mlogger.warn('Exception as err:%s', err)
                MLog.mlogger.warn(traceback.format_exc())
            await asyncio.sleep(0.0001)  # 100 us

            if self.main_thread_exit_flag:
                break
        return

    async def delay_system_startup(self):
        """系统线程延迟启动"""
        await asyncio.sleep(3)  # 延迟3秒启动，让其接收广播包

        # event = EventType.EVENT_SYSTEM_STARTUP
        # event_content = bytes()
        # self.main_event_client.publish_event(event, event_content)

    def signal_handler(self, signum, frame):
        print('Received signal: ', signum)
        # traceback.print_stack()
        self.main_thread_exit_flag = True
        time.sleep(0.5)

    def register_signal(self):
        signal.signal(signal.SIGHUP, self.signal_handler)  # 1
        signal.signal(signal.SIGINT, self.signal_handler)  # 2
        signal.signal(signal.SIGQUIT, self.signal_handler)  # 3
        signal.signal(signal.SIGABRT, self.signal_handler)  # 6
        signal.signal(signal.SIGTERM, self.signal_handler)  # 15
        signal.signal(signal.SIGSEGV, self.signal_handler)  # 11


if __name__ == '__main__':
    main_controller = MainThread()
    os._exit(0)



