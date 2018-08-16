#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 11:32
# @Author  : hedengfeng
# @Site    : 
# @File    : EventClient.py
# @Software: LT_controller

import threading
import traceback

import zmq

from eventbus.EventBus import EventBus
from utility.LTCommon import LTEventType
from utility.Mlogging import MLog


class EventClient(object):
    """
    事件处理的客户端
    """

    def __init__(self):
        """
        在总线上初始化客户端
        :rtype: object
        """
        EventBus.register_client(threading.get_ident(), self)
        self._pub_socket = EventBus.CONTEXT.socket(zmq.PUB)
        self._pub_socket.setsockopt(zmq.SNDTIMEO, 2000)
        self._pub_socket.connect(EventBus.XSUB_ADDR_PORT)

        self._sub_socket = EventBus.CONTEXT.socket(zmq.SUB)
        self._sub_socket.setsockopt(zmq.RCVTIMEO, 2000)
        self._sub_socket.connect(EventBus.XPUB_ADDR_PORT)
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, EventBus.COMMON_SUB_STR)

        self._event_id_target_map = {}  # 事件和 注册这个事件的对象列表 的字典

    def handle_event(self):
        """
        接收EventBus上的message，传递给EventTarget的event_handle
        """
        while self._sub_socket.poll(20):
            try:
                event = self._sub_socket.recv_multipart()
                if event is None:
                    continue
                # while self._sub_socket.getsockopt(zmq.RCVMORE):
                #     event.append(self._sub_socket.recv_multipart(zmq.NOBLOCK))

                try:
                    message = [event[0].decode(), event[1].decode(), event[2]]
                    if message[0] == EventBus.COMMON_SUB_STR:
                        if message[1] in self._event_id_target_map.keys():
                            for target in self._event_id_target_map[message[1]]:
                                target.event_handle(message[1], message[2])
                except TypeError as err:
                    MLog.mlogger.warn('TypeError:%s', err)
                    MLog.mlogger.warn(traceback.format_exc())
            except zmq.error.Again as err:
                MLog.mlogger.warn(err)
                MLog.mlogger.warn(traceback.format_exc())

    def publish_loc_event(self, event, event_content):
        """
        发布一个事件到本地客户端，不到EventBus上，在本客户端的订阅者将会直接调用
        :param event_content: bytes
        :param event: str
        """
        if event in self._event_id_target_map.keys():
            for target in self._event_id_target_map[event]:
                target.event_handle(event, event_content)

    def publish_event(self, event, event_content):
        """
        发布一条信息到eventBus上
        :param event_content: bytes
        :param event: str
        """
        # print('publish event: ', event)
        try:
            self._pub_socket.send_multipart([EventBus.COMMON_SUB_STR.encode(), event.encode(), event_content])
        except TypeError as err:
            MLog.mlogger.warn('TypeError:%s', err)
            MLog.mlogger.warn(traceback.format_exc())
        except zmq.error.Again as err:
            MLog.mlogger.warn(err)
            MLog.mlogger.warn(traceback.format_exc())

    def register_observer(self, event_id, target_object):
        """
        注册一个事件的观察者
        :param event_id: 注册事件的id
        :param target_object: EventTarget 对象
        """
        if event_id in self._event_id_target_map:
            if target_object not in self._event_id_target_map[event_id]:
                self._event_id_target_map[event_id].append(target_object)
        else:
            self._event_id_target_map[event_id] = []
            self._event_id_target_map[event_id].append(target_object)

    def unregister_observer(self, event_id, target_object):
        """
        注销一个事件的观察者
        :param event_id: 注册事件的id
        :param target_object: EventTarget 对象
        """
        if event_id in self._event_id_target_map:
            if target_object in self._event_id_target_map[event_id]:
                self._event_id_target_map[event_id].remove(target_object)

    def __del__(self):
        """"""





