import cv2
import matplotlib.pyplot as plt
from skimage import io, color, feature, exposure
from scipy.spatial import distance

# 加载图像
imageA = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度
imageB = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度

# 应用高斯模糊
blurredImageA = cv2.GaussianBlur(imageA, (251, 251), 0)
blurredImageB = cv2.GaussianBlur(imageB, (201, 201), 0)

# 计算HOG特征
hog1, hog1_image = feature.hog(blurredImageA, visualize=True)
hog2, hog2_image = feature.hog(blurredImageB, visualize=True)

# 计算两个HOG描述符之间的欧几里得距离
hog_distance = distance.euclidean(hog1, hog2)

# 输出HOG描述符之间的距离
print(f'HOG Descriptor Distance: {hog_distance}')

# 可视化HOG图像
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)

ax1.axis('off')
ax1.imshow(hog1_image, cmap=plt.cm.gray)
ax1.set_title('HOG Image 1')

ax2.axis('off')
ax2.imshow(hog2_image, cmap=plt.cm.gray)
ax2.set_title('HOG Image 2')

plt.show()
