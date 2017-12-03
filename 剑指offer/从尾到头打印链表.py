#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/3 17:09'

# 题目描述
# 输入一个链表，从尾到头打印链表每个节点的值。


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


class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, listNode):
        current_head = listNode
        val_list = []
        while current_head:
            val_list.append(current_head.val)
            current_head = current_head.next
        val_list.reverse()
        return val_list


l = List()
l.add(1)
l.add(2)
l.add(3)
l.add(3)
l.add(4)
l.add(4)
l.add(5)
s = Solution()
p = s.printListFromTailToHead(l.head)
pass