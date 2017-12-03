#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/3 13:39'

# 题目描述
# 在一个排序的链表中，存在重复的结点，请删除该链表中重复的结点，重复的结点不保留，返回链表头指针。
# 例如，链表1->2->3->3->4->4->5 处理后为 1->2->5


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
    def deleteOneDuplication(self, pHead):
        """
        在一个排序的链表中，存在重复的结点，删除该链表中重复的结点，返回链表头指针。
        例如，链表1->2->3->3->4->4->5 处理后为 1->2->3->4->5
        遍历链表，删除值重复的节点
        :param pHead: 链表头
        :return: 链表头
        """
        previous_head = None
        current_head = pHead
        node_val_list = []
        while current_head:
            if current_head.val in node_val_list:
                previous_head.next = current_head.next
                current_head = current_head.next
            else:
                node_val_list.append(current_head.val)
                previous_head = current_head
                current_head = current_head.next
        return pHead

    def deleteDuplication(self, pHead):
        """
        在一个排序的链表中，存在重复的结点，删除该链表中重复的结点，重复的结点不保留，返回链表头指针。
        例如，链表1->2->3->3->4->4->5 处理后为 1->2->5
        遍历链表，删除值重复的节点
        :param pHead: 链表头
        :return: 链表头
        """
        if pHead is None or pHead.next is None:
            return pHead
        current_head = pHead
        next_head = pHead.next
        if next_head.val != current_head.val:
            current_head.next = self.deleteDuplication(next_head)
        else:
            while current_head.val == next_head.val and next_head.next is not None:
                next_head = next_head.next
            if current_head.val == next_head.val:
                # 已经到了最后一个节点
                return None
            else:
                current_head = self.deleteDuplication(next_head)
        return current_head



l = List()
l.add(1)
l.add(2)
l.add(3)
l.add(3)
l.add(4)
l.add(4)
l.add(5)
s = Solution()
p = s.deleteDuplication(l.head)
pass
