#!/usr/bin/env python
# encoding: utf-8

import logging

class LogSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        logging.basicConfig(filename='quantLog.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)

