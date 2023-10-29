import cv2
import matplotlib.pyplot as plt
import numpy as np

# 读取图像
image = cv2.imread('img_115_.png', 0)  # 0表示以灰度模式读取图像

# 设定模糊初始和最终半径
initial_blur_radius = 1
final_blur_radius = 251

# 设定模糊半径增量
blur_increment = 50

# 获取图像的尺寸
h, w = image.shape

# 创建x和y坐标的网格
y, x = np.mgrid[0:h, 0:w]

# 创建一个新的图形窗口
fig = plt.figure(figsize=(10, 5 * ((final_blur_radius - initial_blur_radius) // blur_increment + 1)))

# 循环模糊半径值
for i, blur_radius in enumerate(range(initial_blur_radius, final_blur_radius + 1, blur_increment)):
    # 创建子图
    ax = fig.add_subplot((final_blur_radius - initial_blur_radius) // blur_increment + 1, 1, i + 1, projection='3d')

    # 应用高斯模糊
    blurred_image = cv2.GaussianBlur(image, (blur_radius, blur_radius), 0)

    # 绘制三维表面图
    ax.plot_surface(x, y, blurred_image, cmap='hot')
    ax.set_title(f'Blur Radius: {blur_radius}')

# 调整子图间的间距
plt.tight_layout()
# 显示图形
plt.show()
