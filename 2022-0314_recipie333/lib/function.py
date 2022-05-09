#!/usr/bin/env python
# coding: utf-8


import numpy as np
import os

def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_data(path):
    f = open(path,encoding="utf-8",mode="r")  # 上記でエラーが出る場合、utf-8によるエンコーディングを指定
    data = f.read().splitlines()
    f.close()
    return data