import numpy as np

if __name__ == '__main__':
    str_a, str_b = 'BAAC', 'BAC'
    if len(str_a) > len(str_b):
        str_a, str_b = str_b, str_a

    len_a, len_b = len(str_a), len(str_b)

    max_map = {}  # b: [mx_arr] # mx_arr = []  # start_a,start_b,len,b (k 固定为1，b是直线和x轴的交点) # y = x + b => b = y-x

    dp = np.zeros((len_a + 1, len_b + 1), dtype=np.int_)

    for j in range(1, len_b + 1):
        for i in range(1, len_a + 1):
            if str_a[i - 1] == str_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1

            # 判断是否是最大的就可以了对吧
            if dp[i][j] > 0:
                if (j - i) not in max_map:  # 初始化字典的key
                    max_map[j - i] = []

                found = False

                max_arr = max_map[j - i]
                mx = dp[i][j]
                start_a, start_b = i - mx, j - mx
                for items in max_arr:  # abced    abbc
                    if start_a == items[0] and start_b == items[1]:
                        items[2] = mx
                        found = True

                if not found:
                    max_map[j - i].append([start_a, start_b, mx, j - i])

    for key, val in max_map.items():
        for items in val:
            print(str_a[items[0]:items[0] + items[2]])

    # print(start, mx, str_a[start:start + mx])

#     a  b  c  c  e
#   0
# a   1
# b      1
# b      1
# c         1  1
# e                1
