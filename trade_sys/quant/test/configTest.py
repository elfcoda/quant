#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append("..")
from src.config import ConfigSingleton

# 测试单例模式
obj1 = ConfigSingleton()
obj2 = ConfigSingleton()
print(obj1 is obj2)  # 输出 True，说明 obj1 和 obj2 是同一个实例

print(obj1.api_key)
print(obj1.secret_key)
print(obj1.passphrase)
print(obj1.simu_mode)
