#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 18:52
# @Author  : hedengfeng
# @Site    : 
# @File    : MsgTarget.py 所有对象的父类
# @Software: LT_controller

import threading
import traceback

from utility.Mlogging import MLog
from eventbus.EventBus import EventBus
from eventbus.MsgClient import MsgClient


class MsgTarget(object):
    """
    EventBus的Target对象，由该对象的子类处理event消息和发送消息
    """
    _my_client: MsgClient = None

    def __init__(self, child_class):
        """
        在eventBus上找到本身线程的消息客户端
        :rtype: object
        """
        self._child_class = child_class
        self._my_client = EventBus.find_client(threading.get_ident())
        if self._my_client is None:
            MLog.mlogger.warn('not find client: %i' % threading.get_ident())
            traceback.print_stack()

    def event_handle(self, event, event_content):
        """
        事件处理函数，该函数可以理解为纯虚函数，MsgTarget子类必须要实现
        消息客户端接收到消息总线上的数据之后，会调用该函数
        :param event_content: str
        :param event: str
        """
        if self._my_client is not None:
            self._child_class.event_handle(event, event_content)
        else:
            MLog.mlogger.warn('_my_client is not None')

    def publish_event(self, event, event_content):
        """
        通过消息客户端发布一条信息到eventBus上
        :param event_content: str
        :param event: str
        """
        if self._my_client is not None:
            self._my_client.publish_event(event, event_content)
        else:
            MLog.mlogger.warn('_my_client is not None')
            traceback.print_stack()

    def subscribe(self, event_id, object):
        """
        订阅一条消息。
        :param event_id: 消息id
        :param object:子类对象
        """
        if self._my_client is not None:
            self._my_client.register_observer(event_id, object)
        else:
            MLog.mlogger.warn('_my_client is None')
            print('_my_client is None', self)
            traceback.print_stack()

    def unsubscribe(self, event_id, object):
        """
        撤销对一条消息的订阅。
        :param event_id: 消息id
        :param object:子类对象
        """
        if self._my_client is not None:
            self._my_client.unregister_observer(event_id, object)
        else:
            MLog.mlogger.warn('_my_client is not None')

    def __del__(self):
        """"""
        # super(MsgTarget, self).__del__()
