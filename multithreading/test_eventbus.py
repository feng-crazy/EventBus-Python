#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 18:31
# @Author  : hedengfeng
# @Site    : 
# @File    : test_eventbus.py
# @Software: LT_controller
import threading
import time

from eventbus.EventBus import EventBus
from eventbus.MThread import MThread
from eventbus.EventTarget import EventTarget


class TestEventTarget1(EventTarget):
    """
    test EventTarget
    """
    def __init__(self):
        super(TestEventTarget1, self).__init__(self)
        self.subscribe('TestThread2', self)
        self.subscribe('TestEventTarget2', self)
        
    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        print('TestEventTarget1 ', 'event_handle', event, event_content)

    def exec(self):
        """
            publish_event
        """
        event = 'TestEventTarget1'
        event_content = (str(time.time())).encode()
        print('publish_event:', event, event_content)
        self.publish_event(event, event_content)
        
    def __del__(self):
        self.unsubscribe('TestThread2', self)
        self.unsubscribe('TestEventTarget2', self)
        super(TestEventTarget1, self).__del__()


class TestEventTarget2(EventTarget):
    """
    test EventTarget
    """

    def __init__(self):
        super(TestEventTarget2, self).__init__(self)
        self.subscribe('TestThread1', self)
        self.subscribe('TestEventTarget1', self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        print('TestEventTarget2 ', 'event_handle', event, event_content)

    def exec(self):
        """
            publish_event
        """
        event = 'TestEventTarget2'
        event_content = (str(time.time())).encode()
        self.publish_event(event, event_content)
        print('publish_event:', event, event_content)

    def __del__(self):
        self.unsubscribe('TestThread1')
        self.unsubscribe('TestEventTarget1')
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
        event = 'TestThread1'
        event_content = str(time.time())
        print('publish_event:', event, event_content)
        self.publish_event(event, event_content)
        self.test_target1.exec()
        time.sleep(2)
        print('TestThread1..............................time.sleep(2)')

    def setup_thread(self):
        """
        子线程初始操作函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        EventTarget.__init__(self, self)  # 该父类的构造必须是要再该线程执行中，最开始执行
        print('setup_thread...........', threading.current_thread(), self.thread_name)
        self.test_target1 = TestEventTarget1()
        self.subscribe('TestThread2', self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        print('TestThread1 ' 'event_handle', event, event_content)

    def __del__(self):
        self.unsubscribe('TestThread2', self)
        super(TestThread1, self).__del__(self)


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
        event = 'TestThread2'
        event_content = str(time.time())
        print('publish_event:', event, event_content)
        self.publish_event(event, event_content)
        self.test_target2.exec()
        time.sleep(2)
        print('TestThread2..............................time.sleep(2)')

    def setup_thread(self):
        """
        子线程初始操作函数，该函数可以理解为纯虚函数，MThread子类必须要实现
        """
        EventTarget.__init__(self, self)  # 该父类的构造必须是要再该线程执行中，最开始执行

        print('setup_thread...........', threading.current_thread(), self.thread_name)
        self.test_target2 = TestEventTarget2()

        self.subscribe('TestThread1', self)

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        """
        print('TestThread2 ', 'event_handle', event, event_content)

    def __del__(self):
        self.unsubscribe('TestThread1', self)
        super(TestThread2, self).__del__(self)


if __name__ == '__main__':
    eventbus = EventBus()
    thread_1 = TestThread1('thread_1')
    thread_1.start()

    thread_2 = TestThread2('thread_1')
    thread_2.start()

    while True:
        time.sleep(1)
        pass
