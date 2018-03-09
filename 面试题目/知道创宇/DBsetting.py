#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
import sqlite3
import os
import logging


class MySQLite:
    def __init__(self, filename):
        """
        初始化数据库文件
        :param filename:文件名
        """
        ls = os.listdir('.')
        exist = True if filename in ls else False
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.db.cursor()
        if not exist:
            # 如果不存在该文件则创建并创建新表
            try:
                sql = 'CREATE TABLE spider(id INTEGER PRIMARY KEY, url TEXT, content TEXT)'
                self.c.execute(sql)
                self.db.commit()
            except :
                logging.error(filename + ' 创建表格错误')

    def insert(self, url, content):
        """
        插入数据
        :param url: url
        :param content: 网页内容
        """
        self.c.execute('INSERT INTO spider(url, content) VALUES(?, ?)', (url, content))
        self.db.commit()