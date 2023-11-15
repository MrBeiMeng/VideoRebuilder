import math


def find_min_multiplier_and_divisor(value):
    multiplier = 1
    # divisor = 1

    # 查找最小乘数
    while True:
        result = value * multiplier
        print(f'{result} = {value} * {multiplier}')
        if math.isclose(result, round(result), rel_tol=1e-9):
            break  # 如果结果接近于一个整数，那么已经找到了最小乘数
        multiplier += 1

    # # 查找最小除数
    # while True:
    #     result = value / divisor
    #     if math.isclose(result, round(result), rel_tol=1e-9):
    #         break  # 如果结果接近于一个整数，那么已经找到了最小除数
    #     divisor += 1

    return multiplier


# 测试函数
value = 1.489
multiplier = find_min_multiplier_and_divisor(value)
print(f'Minimum Multiplier: {multiplier}')
