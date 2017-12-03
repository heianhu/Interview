#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/3 02:03'

# 题目描述
# 一个链表中包含环，请找出该链表的环的入口结点。


class ListNode(object):
    def __init__(self, x=None, nextNode=None):
        self.val = x
        self.next = nextNode


class List(object):
    def __init__(self):
        self.head = ListNode()

    def isEmpty(self):
        return True if self.head.val is None else False

    def add(self, x, nextNode=None):
        if self.isEmpty():
            self.head.val = x
        else:
            phead = self.head
            while phead.next is not None:
                phead = phead.next
            phead.next = ListNode(x, nextNode)


class Solution(object):
    def EntryNodeOfLoop(self, pHead):
        """
        遍历链表，环的存在，遍历遇见的第一个重复的即为入口节点
        :param pHead:
        :return:
        """
        nodeList = []   # 将每个节点加入，判断节点是否相同，即判断所在的内存是否相同
        p = pHead
        while p is not None:
            if p in nodeList:
                return p
            else:
                nodeList.append(p)
            p = p.next


l = List()
l.add(1)
l.add(2)
l.add(3, l.head)
s = Solution()
p = s.EntryNodeOfLoop(l.head)
pass