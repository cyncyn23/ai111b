import random
import numpy as np
import matplotlib.pyplot as plt

# 定義目標函數
def cost_func(X, Y, a, b):
    return np.sum((Y - (a * X + b)) ** 2)

# 隨機產生一條回歸線
def init_params():
    return random.uniform(-10, 10), random.uniform(-10, 10)

# 移動策略
def move(a, b):
    # 隨機改變斜率或截距
    if random.random() < 0.5:
        a += random.uniform(-0.1, 0.1)
    else:
        b += random.uniform(-0.1, 0.1)
    return a, b

# 爬山演算法
def hill_climbing(X, Y, max_iter=1000, threshold=1e-6):
    # 隨機初始化
    a, b = init_params()
    cost = cost_func(X, Y, a, b)
    costs = [cost]
    for i in range(max_iter):
        # 移動
        a_new, b_new = move(a, b)
        cost_new = cost_func(X, Y, a_new, b_new)
        # 判斷是否更好
        if cost_new < cost:
            a, b = a_new, b_new
            cost = cost_new
        # 判斷終止條件
        if cost < threshold:
            break
        costs.append(cost)
    return a, b, costs

# 產生數據
X = np.linspace(-10, 10, 100)
Y = 2 * X + 3 + np.random.normal(0, 1, 100)

# 執行爬山演算法
a, b, costs = hill_climbing(X, Y)

# 繪製結果
plt.scatter(X, Y)
plt.plot(X, a * X + b, color='red')
plt.title('Regression line by Hill Climbing Algorithm')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
