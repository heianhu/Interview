#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/5 00:55'

# 题目描述
# 一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法。


class Solution:
    def jumpFloor(self, number):
        jumpfloor = [0, 1, 2]
        if number > 2:
            for i in range(3, number+1):
                jumpfloor.append(jumpfloor[i-2] + jumpfloor[i-1])
        return jumpfloor[number]

# 1 1
# 2 2
# 3 3
# 4 5
# 5 8
