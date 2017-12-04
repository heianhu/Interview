#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'
__data__ = '2017/12/5 01:32'

# 题目描述
# 我们可以用2*1的小矩形横着或者竖着去覆盖更大的矩形。请问用n个2*1的小矩形无重叠地覆盖一个2*n的大矩形，总共有多少种方法？


class Solution:
    def rectCover(self, number):
        fibonacci = [0, 1]
        if number > 1:
            number += 1
            for i in range(2, number + 1):
                fibonacci.append(fibonacci[i - 2] + fibonacci[i - 1])
        return fibonacci[number]


s = Solution()
print(s.rectCover(0))

# 1 1
# 2 2
# 3 3
# 4 5
# 即斐波那契数列

# 网友思路
# 依旧是斐波那契数列
# 2 * n的大矩形，和n个2 * 1
# 的小矩形
# 其中target * 2
# 为大矩阵的大小
# 有以下几种情形：
# target <= 0 大矩形为<= 2*0,直接return 1；
# target = 1大矩形为2*1，只有一种摆放方法，return1；
# target = 2 大矩形为2*2，有两种摆放方法，return2；
# target = n 分为两步考虑：
#     第一次摆放一块 2*1 的小矩阵，则摆放方法总共为f(target - 1)
#     [√][ ][ ][ ]...
#     [√][ ][ ][ ]...
#     第一次摆放一块1 * 2
#     的小矩阵，则摆放方法总共为f(target - 2)
#     因为，摆放了一块1 * 2
#     的小矩阵（用√√表示），对应下方的1 * 2（用××表示）摆放方法就确定了，所以为f(targte - 2)
#     [√][√][ ][ ]...
#     [x][x][ ][ ]...