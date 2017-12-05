#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/6 00:09'


# 题目描述
# 给定一个数组和滑动窗口的大小，找出所有滑动窗口里数值的最大值。
# 例如，如果输入数组{2,3,4,2,6,2,5,1}及滑动窗口的大小3，那么一共存在6个滑动窗口，他们的最大值分别为{4,4,6,6,6,5}；
# 针对数组{2,3,4,2,6,2,5,1}的滑动窗口有以下6个：
# {[2,3,4],2,6,2,5,1}
# {2,[3,4,2],6,2,5,1}
# {2,3,[4,2,6],2,5,1}
# {2,3,4,[2,6,2],5,1}
# {2,3,4,2,[6,2,5],1}
# {2,3,4,2,6,[2,5,1]}

class Solution:
    def maxInWindows(self, num, size):
        """
        含有所有滑动窗口里数值的最大值的list
        :param num: 滑动窗口数组
        :param size: 滑动窗口大小
        :return:
        """
        max_list = []
        if size > 0:
            for i in range(len(num)-size+1):
                max_list.append(max(num[i:i+size]))
        return max_list


s = Solution()
print(s.maxInWindows([10, 14, 12, 11], 0))
