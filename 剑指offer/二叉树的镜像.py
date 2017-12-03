#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/3 00:22'

# 题目描述
# 操作给定的二叉树，将其变换为源二叉树的镜像。
# 输入描述:
# 二叉树的镜像定义：源二叉树
#     	    8
#     	   /  \
#     	  6   10
#     	 / \  / \
#     	5  7 9 11
#     	镜像二叉树
#     	    8
#     	   /  \
#     	  10   6
#     	 / \  / \
#     	11 9 7  5


class TreeNode(object):
    def __init__(self, x=None, left=None, right=None):
        self.val = x
        self.left = left
        self.right = right


class Tree(object):
    def __init__(self):
        self.root = TreeNode()

    def add(self, x):
        node = TreeNode(x)
        if self.isEmpty():
            self.root = node
        else:
            queue = [self.root]
            while queue:
                treenode = queue.pop(0)
                if treenode.left is None:
                    treenode.left = node
                    return
                elif treenode.right is None:
                    treenode.right = node
                    return
                else:
                    queue.append(treenode.left)
                    queue.append(treenode.right)

    def isEmpty(self):
        return True if self.root.val is None else False

    def print(self):
        if self.root is not None:
            queue = [self.root]
            while len(queue) > 0:
                curLevel, count = len(queue), 0
                print()
                while count < curLevel:
                    count += 1
                    proot = queue.pop(0)
                    print(proot.val, end=' ')
                    if proot.left:
                        queue.append(proot.left)
                    if proot.right:
                        queue.append(proot.right)


class Solution(object):
    def Mirror(self, root):
        """
        返回镜像树的根节点
        :param root:
        :return:
        """
        # root = self.root
        if root is not None:
            queue = [root]
            while len(queue) > 0:
                proot = queue.pop(0)
                proot.left, proot.right = proot.right, proot.left
                if proot.left:
                    queue.append(proot.left)
                if proot.right:
                    queue.append(proot.right)


tree = Tree()
tree.add(8)
tree.add(6)
tree.add(10)
tree.add(5)
tree.add(7)
tree.add(9)
tree.add(11)
tree.print()
s = Solution()
s.Mirror(tree.root)
print()
tree.print()

