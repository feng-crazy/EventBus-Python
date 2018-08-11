#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 11:32
# @Author  : hedengfeng
# @Site    : 
# @File    : MsgClient.py
# @Software: LT_controller

import threading

import zmq

from eventbus.EventBus import EventBus


class MsgClient(object):
    """
    消息处理的客户端
    """

    def __init__(self):
        """
        在总线上初始化客户端
        :rtype: object
        """
        EventBus.register_client(threading.get_ident(), self)
        self._pub_socket = EventBus.CONTEXT.socket(zmq.PUB)
        self._pub_socket.connect(EventBus.XSUB_ADDR_PORT)

        self._sub_socket = EventBus.CONTEXT.socket(zmq.SUB)
        self._sub_socket.connect(EventBus.XPUB_ADDR_PORT)
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, EventBus.COMMON_SUB_STR)

        self._event_id_target_map = {}

    def handle_event(self):
        """
        接收EventBus上的message，传递给MsgTarget的event_handle
        """
        while self._sub_socket.poll(20):
            event = self._sub_socket.recv_multipart(zmq.NOBLOCK)
            if event is None:
                continue
            # while self._sub_socket.getsockopt(zmq.RCVMORE):
            #     event.append(self._sub_socket.recv_multipart(zmq.NOBLOCK))

            message = [event[0].decode(), event[1].decode(), event[2].decode()]
            if message[0] == EventBus.COMMON_SUB_STR:
                if message[1] in self._event_id_target_map.keys():
                    for target in self._event_id_target_map[message[1]]:
                        target.event_handle(message[1], message[2])

    def publish_event(self, event, event_content):
        """
        发布一条信息到eventBus上
        :param event_content: str
        :param event: str
        """
        # print('publish event: ', event)
        self._pub_socket.send_multipart([EventBus.COMMON_SUB_STR.encode(), event.encode(), event_content.encode()])

    def register_observer(self, event_id, object):
        """
        注册一个消息的观察者
        :param event_id: 注册消息的id
        :param object: MsgTarget 对象
        """
        if event_id in self._event_id_target_map:
            if object not in self._event_id_target_map[event_id]:
                self._event_id_target_map[event_id].append(object)
        else:
            self._event_id_target_map[event_id] = []
            self._event_id_target_map[event_id].append(object)

    def unregister_observer(self, event_id, object):
        """
        注销一个消息的观察者
        :param event_id: 注册消息的id
        :param object: MsgTarget 对象
        """
        if event_id in self._event_id_target_map:
            if object in self._event_id_target_map[event_id]:
                self._event_id_target_map[event_id].remove(object)
                
    def __del__(self):
        """"""



