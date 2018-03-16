#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'

"""
以下是后台的代码面试题，如果觉得搞定了，可以联系我：

使用 Python 编写一个网站爬虫程序，支持参数如下：
spider.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number --dbfile  filepath  --key="HTML5"
# -u -d -f -l
参数说明：
-u 指定爬虫开始地址
-d 指定爬虫深度
--thread 指定线程池大小，多线程爬取页面，可选参数，默认10
--dbfile 存放结果数据到指定的数据库（sqlite）文件中
--key 页面内的关键词，获取满足该关键词的网页，可选参数，默认为所有页面
-l 日志记录文件记录详细程度，数字越大记录越详细，可选参数，默认spider.log
--testself 程序自测，可选参数

功能描述：
1、指定网站爬取指定深度的页面，将包含指定关键词的页面内容存放到sqlite3数据库文件中
2、程序每隔10秒在屏幕上打印进度信息
3、支持线程池机制，并发爬取网页
4、代码需要详尽的注释，自己需要深刻理解该程序所涉及到的各类知识点
5、需要自己实现线程池

提示1：使用 re、urllib/urllib2、beautifulsoup/lxml2、threading、optparse、Queue、sqlite3、logger、doctest 等模块
提示2：注意是"线程池"而不仅仅是多线程
提示3：爬取 sina.com.cn 或其它你喜欢的目标网站，要求两级深度要能正常结束

建议程序可分阶段，逐步完成编写，例如：
版本1：spider1.py -u url -d deep
版本2：spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself
版本3：spider3.py -u url -d deep -f logfile -l loglevel(1-5)  --testself -thread number
版本4：剩下所有功能
"""

import time
import sys
import getopt
import threading
import os
import queue
import curses  # 文本交互
import logging  # 日志https://docs.python.org/3.6/library/logging.html
from myError import *
from DBsetting import MySQLite
import requests
from bs4 import BeautifulSoup
import lxml
import urllib.parse
from utils import get_md5


def run_spider(thread_num, link, deep, key):
    """
    控制函数
    :param thread_num: 线程数
    :param link: 主url
    :param deep: 深度
    :param key: 关键词
    """
    event = threading.Event()
    event.clear()
    pool = ThreadPool(thread_num, event)
    UI(pool.get_queue(), deep, event)
    pool.push((link, deep), key)
    pool.wait()


class UI(threading.Thread):
    """
    UI类
    """

    def __init__(self, queuelinks, deep, event):
        threading.Thread.__init__(self)
        self.queuelinks = queuelinks
        self.deep = deep
        self.event = event
        self.start()

    def run(self):
        if deep == 0:
            print('第 {0} 层: {1:%}%'.format(1, 1))
            return
        screen = curses.initscr()  # 初始化终端界面输出窗口
        max_file = [0] * (self.deep + 1)
        while True:
            links = list(self.queuelinks.__dict__['queue'])
            # 队列中每个URL此时的深度值
            deeps = [x[1] for x in links]
            keys = [[x, 0] for x in range(self.deep + 1)]
            n = len(keys)
            for d in deeps:
                keys[d][1] += 1
            screen.clear()  # 清屏，等待输出
            count = 0
            for d in range(1, n + 1):
                count += 1
                if keys[n - d][1] > max_file[d - 1]:
                    max_file[d - 1] = keys[n - d][1]
                if max_file[d - 1] == 0:
                    num = 1
                else:
                    num = 1 - (keys[n - d][1] / max_file[d - 1])
                screen.addstr(count, 0, '第 {0} 层: {1:%}%'.format(d, num))
            screen.refresh()  # 使生效
            time.sleep(0.2)
            if self.event.is_set():
                curses.endwin()
                logging.info('完成于: ' + time.ctime())
                break


class Spider(threading.Thread):
    """
    爬虫类
    """
    urls = set()  # url集合防止重复
    fileMD5 = set()  # 文件的MD5，防止重复

    def __init__(self, queuelinks, key, rlock):
        """
        初始化爬虫
        :param queuelinks:线程队列
        :param key:关键词
        :param rlock: 多重锁
        """
        threading.Thread.__init__(self)
        self.queue = queuelinks
        self.keyList = key
        self.rlock = rlock
        self.link = None
        self.deep = None
        self.key = None
        self.setDaemon(True)  # 父线程结束后，子线程也相应结束
        self.start()

    @classmethod
    def _deal_repetitive_filename(cls, name):
        """
        当名字相同但是页面内容不同时
        :param name: url改写的文件名
        :return: 新的文件名
        """
        try:
            files = os.listdir('.')
        except:
            logging.error('无法读取本目录下的文件')  # 写入错误日志
        else:
            count = 1
            while True:
                if name in files:
                    name = '.'.join([name, str(count)])
                    count += 1
                else:
                    return name

    def _get_response(self, url):
        """
        访问请求
        :param url: 访问页面的url
        :return: response
        """
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        }
        response = requests.get(url, headers=headers)
        return response

    def save_file(self):
        """
        将数据保存到本地
        """
        name = self.link.replace('/', '_')
        name = self._deal_repetitive_filename(name)
        try:
            data = self._get_response(self.link).text
            md5 = get_md5(data)
            if md5 in self.fileMD5:
                raise SameFileError
            else:
                self.fileMD5.add(md5)
                with open(name, 'w') as f:
                    f.write(data)
        except SameFileError:
            logging.info(self.link + ' 出现相同的内容，已丢弃')  # 写入信息日志

    def save_database(self):
        """
        将数据保存到数据库
        """
        data = self._get_response(self.link).text
        if not data:
            return
        if self.key in data:  # 在页面中找到关键字则放到数据库中
            self.rlock.acquire()
            mysqlite.insert(self.link, data)
            self.rlock.release()

    def get_urls(self):
        """
        将该页面的所有url提取出来
        :return: 该页面所含的url
        """
        soup = BeautifulSoup(self._get_response(self.link).text, 'lxml')
        all_url = []
        for a in soup.find_all('a'):
            all_url.append(urllib.parse.urljoin(self.link, a.get('href')))  # 取得当前a标签的href属性值并将其值放入
        for iframe in soup.find_all('iframe'):
            all_url.append(urllib.parse.urljoin(self.link, iframe.get('src')))  # 取得当前iframe标签的src属性值并将其值放入
        return all_url

    def run(self):
        while True:
            try:
                self.link, self.deep = self.queue.get(timeout=2)
                self.key = self.keyList[0]
            except queue.Empty:
                continue
            if self.deep > 0:
                self.deep -= 1
                links = self.get_urls()
                if links:
                    for i in links:
                        if i not in self.urls:
                            self.urls.add(i)
                            self.queue.put((i, self.deep))
                self.queue.put((self.link, 0))
            else:
                if not self.key:
                    self.save_file()
                else:
                    self.save_database()
                logging.info(self.link + '  [' + str(self.deep) + ']')  # 写入日志
            self.queue.task_done()


class ThreadPool:
    """
    连接池类
    """

    def __init__(self, num, event):
        self.num = num
        self.event = event
        self.threads = []
        self.queue = queue.Queue()
        self.key = [None]
        self.create_thread()

    def create_thread(self):
        """
        创建线程
        """
        for i in range(self.num):
            self.threads.append(Spider(self.queue, self.key, rlock))

    def push(self, job, key=None):
        """
        在线程队列中加入任务
        :param job: (url,deep)
        :param key: 关键字
        :return: 
        """
        self.queue.put(job)
        self.key[0] = key

    def get_queue(self):
        return self.queue

    def wait(self):
        self.queue.join()
        self.event.set()  # 通知显示模块程序结束，关闭进度显示


if __name__ == '__main__':
    url = None  # 默认参数开始
    deep = '1'
    logfile = 'heianhu_spider.log'
    level = '4'
    thread_num = '10'
    dbfile = 'spider.db'
    key = None  # 默认参数结束
    optlist, args = getopt.getopt(
        sys.argv[1:],
        'u:d:f:l:',
        ['thread=', 'dbfile=', 'key='])
    for k, v in optlist:
        if k == '-u':
            url = v
        elif k == '-d':
            deep = v
        elif k == '-f':
            logfile = v
        elif k == '-l':
            level = v
        elif k == '--thread':
            thread_num = v
        elif k == '--dbfile':
            dbfile = v
        elif k == '--key':
            key = v

    deep = int(deep)
    level = int(level)
    thread_num = int(thread_num)
    if level < 1 or level > 5 or deep < 1 or thread_num < 1 or not url:
        raise ParameterError('参数错误，请重新检查！')
    deep -= 1
    if key:
        mysqlite = MySQLite(dbfile)
    logLevel = {
        1: logging.CRITICAL,  # 粗略内容
        2: logging.ERROR,
        3: logging.WARNING,
        4: logging.INFO,
        5: logging.DEBUG,  # 详细内容
    }
    logging.basicConfig(filename=logfile, level=logLevel[level])
    rlock = threading.RLock()  # 多重锁
    run_spider(thread_num, url, deep, key)
