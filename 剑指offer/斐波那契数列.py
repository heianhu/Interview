#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/5 00:39'

# 题目描述
# 大家都知道斐波那契数列，现在要求输入一个整数n，请你输出斐波那契数列的第n项。
# n<=39


class Solution:
    def Fibonacci(self, n):
        fibonacci = [0, 1]
        if n > 1:
            for i in range(2, n+1):
                fibonacci.append(fibonacci[i-2] + fibonacci[i-1])
        return fibonacci[n]


f = Solution()
print(f.Fibonacci(50))
