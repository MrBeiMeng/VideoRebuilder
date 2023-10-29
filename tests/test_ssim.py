import cv2
from skimage.metrics import structural_similarity as compare_ssim

# 加载图像
imageA = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度
imageB = cv2.imread('img_115_.png', cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度

# 应用高斯模糊
blurredImageA = cv2.GaussianBlur(imageA, (251, 251), 0)
blurredImageB = cv2.GaussianBlur(imageB, (201, 201), 0)

# 确保两个图像具有相同的尺寸
assert imageA.shape == imageB.shape, "图像必须具有相同的尺寸"

# 计算SSIM
ssim_value, _ = compare_ssim(blurredImageA, blurredImageB, full=True)

print(f'SSIM: {ssim_value}')
