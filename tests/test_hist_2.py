import cv2
from skimage.metrics import structural_similarity as compare_ssim

# 加载图像
imageA = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度
imageB = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度

# 应用高斯模糊
blurredImageA = cv2.GaussianBlur(imageA, (251, 251), 0)
blurredImageB = cv2.GaussianBlur(imageB, (201, 201), 0)

# 计算图像的直方图
hist1 = cv2.calcHist([blurredImageA], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([blurredImageB], [0], None, [256], [0, 256])

# 归一化直方图
hist1 = cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
hist2 = cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

# 比较直方图
correl = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)  # 相关性比较
chi_square = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)  # 卡方比较
intersection = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)  # 交集比较
bhattacharyya_distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)  # 巴氏距离

# 输出结果
print(f'Correlation: {correl}')
print(f'Chi-Square: {chi_square}')
print(f'Intersection: {intersection}')
print(f'Bhattacharyya Distance: {bhattacharyya_distance}')