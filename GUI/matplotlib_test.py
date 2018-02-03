import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])
plt.ion()

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05)

while True:
    plt.pause(0.05)
# 坐标放大百倍变成ray_tracing里面的坐标
# 设计多种平面图形 每个图形一个class，class内含三视图投影的平面图形构建函数
# 此图（三视图）显示在GUI中