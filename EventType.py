#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 14:10
# @Author  : hedengfeng
# @Site    : 
# @File    : LTCommon.py
# @Software: LT_controller


class EventType(object):
    """
    系统事件类型定义
    """
    EVENT_SYSTEM_STARTUP = 'system startup event'  # 系统启动事件
    EVENT_SYSTEM_TIME_1 = 'once per second'  # 系统每秒一次的定时事件

    """
    独立事件定义
    """
    EVENT_TEST_TARGET_1 = 'test target 1'
    EVENT_TEST_TARGET_2 = 'test target 2'
    EVENT_TEST_THREAD_1 = 'test thread 1'
    EVENT_TEST_THREAD_2 = 'test thread 2'

