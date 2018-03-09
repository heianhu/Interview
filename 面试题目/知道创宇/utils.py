#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'heianhu'

import hashlib


def get_md5(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()
