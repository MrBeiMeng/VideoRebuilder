import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl


def resize_image(image, target_width=1080):
    # 获取图像的原始宽度和高度
    original_width, original_height = image.shape[1], image.shape[0]

    # 计算新的高度，以保持宽高比不变
    new_height = int((target_width / original_width) * original_height)

    # 使用cv2.resize放大图像
    resized_image = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_LINEAR)

    return resized_image


# 加载图像
imageA = cv2.imread("E:/360MoveData/Users/MrB/Pictures/yes.png",
                    cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度
imageB = cv2.imread("E:/360MoveData/Users/MrB/Pictures/yes.png",
                    cv2.IMREAD_GRAYSCALE)  # 加载图像并转换为灰度

imageA = resize_image(imageA, target_width=481)
imageB = resize_image(imageB, target_width=481)

# 应用高斯模糊
# blurredImageA = cv2.GaussianBlur(imageA, (11, 11), 0)
# blurredImageB = cv2.GaussianBlur(imageB, (17, 17), 0)

blurredImageA = imageA
blurredImageB = resize_image(resize_image(imageB, target_width=11), target_width=blurredImageA.shape[1])

# 获取图像B的尺寸
height, width = imageA.shape[:2]

# 裁剪图像A以使其尺寸与图像B相同
blurredImageB = imageB[:height, :width]

# 定义边缘检测卷积核，例如Sobel卷积核
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# 应用边缘卷积
edge_convolved_imageA = cv2.filter2D(blurredImageA, -1, sobel_x)
edge_convolved_imageB = cv2.filter2D(blurredImageB, -1, sobel_x)

# 确保两个图像具有相同的尺寸
assert imageA.shape == imageB.shape, "图像必须具有相同的尺寸"

TwoPFastDtwSiftImpl.draw_matches(0, blurredImageA, blurredImageB)
# 计算SSIM
ssim_value, _ = compare_ssim(edge_convolved_imageA, edge_convolved_imageB, full=True)

print(f'SSIM: {ssim_value}')

TwoPFastDtwSiftImpl.draw_matches(0, edge_convolved_imageA, edge_convolved_imageB)
