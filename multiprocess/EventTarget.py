#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 18:52
# @Author  : hedengfeng
# @Site    : 
# @File    : EventTarget.py 所有对象的父类
# @Software: LT_controller

import threading
import traceback

from utility.Mlogging import MLog
from eventbus.EventBus import EventBus


class EventTarget(object):
    """
    EventBus的Target对象，由该对象的子类处理event事件和发送事件
    """
    _my_client = None

    # 改构造必须要再子类构造之前构造
    def __init__(self, child_class):
        """
        在eventBus上找到本身线程的事件处理者
        :rtype: object
        """
        self._child_class = child_class
        self._my_client = EventBus.find_client(threading.get_ident())
        if self._my_client is None:
            MLog.mlogger.warn('not find client: %i' % threading.get_ident())
            traceback.print_stack()

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，EventTarget子类必须要实现
        事件客户端接收到事件总线上的数据之后，会调用该函数
        :param event_content: bytes
        :param event: str
        """
        if self._my_client is not None:
            self._child_class.event_handle(event, event_content)
        else:
            MLog.mlogger.warn('_my_client is not None')

    def publish_event(self, event, event_content):
        """
        通过事件客户端发布一条信息到eventBus上
        :param event_content: bytes
        :param event: str
        """
        if self._my_client is not None:
            self._my_client.publish_event(event, event_content)
        else:
            MLog.mlogger.warn('_my_client is not None')
            traceback.print_stack()

    def publish_loc_event(self, event, event_content):
        """
        发布一个事件到本地客户端，不到EventBus上，在本客户端的订阅者将会直接调用
        :param event_content: bytes
        :param event: str
        """
        if self._my_client is not None:
            self._my_client.publish_loc_event(event, event_content)
        else:
            MLog.mlogger.warn('_my_client is not None')
            # traceback.print_stack()

    def subscribe(self, event_id, target_object):
        """
        订阅一条事件。
        :param event_id: 事件id
        :param target_object:子类对象
        """
        if self._my_client is not None:
            self._my_client.register_observer(event_id, target_object)
        else:
            MLog.mlogger.warn('_my_client is None')
            # traceback.print_stack()

    def unsubscribe(self, event_id, target_object):
        """
        撤销对一条事件的订阅。
        :param event_id: 事件id
        :param target_object:子类对象
        """
        if self._my_client is not None:
            self._my_client.unregister_observer(event_id, target_object)
        else:
            MLog.mlogger.warn('_my_client is not None')

    def __del__(self):
        """"""
        # print('EventTarget __del__', self._child_class)
        # super(EventTarget, self).__del__()
