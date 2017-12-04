#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/5 01:07'

# 题目描述
# 一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。


class Solution:
    def jumpFloorII(self, number):
        # jumpfloorII = [1, 1]
        # if number > 1:
        #     for i in range(2, number+1):
        #         sum = 0
        #         for i in range(i):
        #             sum += jumpfloorII[i]
        #         jumpfloorII.append(sum)
        # return jumpfloorII[number]
        return 2 ** (number-1)


s = Solution()
print(s.jumpFloorII(5))

# 1 1
# 2 2
# 3 4
# 4 8
# 5 16
# n j(1)+j(2)+...+j(n-1)+1
# 即
# f(1) = 1
# f(2) = f(2-1) + f(2-2)
# f(3) = f(3-1) + f(3-2) + f(3-3)
# ...
# f(n) = f(n-1) + f(n-2) + f(n-3) + ... + f(n-(n-1)) + f(n-n)

# 后来仔细发现，f(n)=n^(n-1)
