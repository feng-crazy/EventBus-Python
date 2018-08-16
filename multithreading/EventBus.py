#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 17:26
# @Author  : hedengfeng
# @Site    : 
# @File    : EventBus.py
# @Software: LT_controller
import threading
import time

import zmq


class EventBus(object):
    """EventBus 由xsub和xpub做总线"""
    XSUB_ADDR_PORT = 'inproc://*:61001'
    XPUB_ADDR_PORT = 'inproc://*:61002'
    CONTEXT = zmq.Context()
    COMMON_SUB_STR = 'common sub str'

    _thread_client_map = {}

    def __init__(self):
        # 创建线程
        self.thread = threading.Thread(target=self.create_eventbus, name='ProxyThread')
        self.thread.start()

    def create_eventbus(self):
        """
        xsub 和xpub构建事件传输的总线
        """
        xsubsocket = EventBus.CONTEXT.socket(zmq.XSUB)
        xsubsocket.bind(EventBus.XSUB_ADDR_PORT)

        xpubsocket = EventBus.CONTEXT.socket(zmq.XPUB)
        xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
        xpubsocket.bind(EventBus.XPUB_ADDR_PORT)

        zmq.proxy(xpubsocket, xsubsocket)

    @classmethod
    def register_client(cls, client_id, client):
        """
        添加一个事件客户端和其对应的id
        :param client_id: 线程id
        :param client:线程id的事件客户端
        """
        print('register_client: client_id:%d' % client_id)
        cls._thread_client_map[client_id] = client

    @classmethod
    def find_client(cls, client_id):
        """
        根据id找到线程的客户端
        :param client_id:寻找线程的id
        """
        if client_id in cls._thread_client_map:
            return cls._thread_client_map[client_id]

    def __del__(self):
        super(EventBus, self).__del__()


def test1():
    xpub_socket = EventBus.CONTEXT.socket(zmq.PUB)
    xpub_socket.connect(EventBus.XSUB_ADDR_PORT)

    xsub_socket = EventBus.CONTEXT.socket(zmq.SUB)
    xsub_socket.connect(EventBus.XPUB_ADDR_PORT)
    xsub_socket.setsockopt_string(zmq.SUBSCRIBE, "test2")
    xsub_socket.setsockopt_string(zmq.SUBSCRIBE, "test1")

    cnt = 0
    while True:
        cnt += 1
        pub_timestamp = time.time()
        xpub_socket.send_string("test1:" + "%i,%i" % (pub_timestamp, cnt))

        while xsub_socket.poll(20):
            msg = xsub_socket.recv_string(zmq.NOBLOCK)
            if msg is None:
                break
            while xsub_socket.getsockopt(zmq.RCVMORE):
                msg.append(xsub_socket.recv_string(zmq.NOBLOCK))
            print('test1: ', msg, len(msg))

        time.sleep(0.4)


def test2():
    xpub_socket = EventBus.CONTEXT.socket(zmq.PUB)
    xpub_socket.connect(EventBus.XSUB_ADDR_PORT)

    xsub_socket = EventBus.CONTEXT.socket(zmq.SUB)
    xsub_socket.connect(EventBus.XPUB_ADDR_PORT)
    xsub_socket.setsockopt_string(zmq.SUBSCRIBE, "test1")

    cnt = 0
    while True:
        cnt += 1
        pub_timestamp = time.time()
        xpub_socket.send_string("test2:" + "%i,%i" % (pub_timestamp, cnt))

        while xsub_socket.poll(20):
            msg = xsub_socket.recv_string(zmq.NOBLOCK)
            if msg is None:
                break
            while xsub_socket.getsockopt(zmq.RCVMORE):
                msg.append(xsub_socket.recv_string(zmq.NOBLOCK))
            print('test2: ', msg, len(msg))

        time.sleep(0.2)


if __name__ == '__main__':
    event_bus = EventBus()
    thread1 = threading.Thread(target=test1, name='test1Thread')
    thread1.start()

    thread2 = threading.Thread(target=test2, name='test1Thread')
    thread2.start()
