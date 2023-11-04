import cv2
import numpy as np

from src.heigher_service.impl.two_p_fast_dtw_sift_impl import TwoPFastDtwSiftImpl


def split_image(image, width):
    # 获取图片的宽度，并计算分割的数量
    img_width = image.shape[1]
    n_splits = img_width // width
    # 分割图片，并将分割块存储到数组中
    splits = [image[:, i * width:(i + 1) * width] for i in range(n_splits)]
    return splits


def paint_blocks(blocks, is_odd):
    # 复制一份分割块数组
    painted_blocks = [block.copy() for block in blocks]
    for i, block in enumerate(painted_blocks):
        if (is_odd and i % 2 == 0) or (not is_odd and i % 2 != 0):
            # if i + 1 < len(painted_blocks):
            #     temp = painted_blocks[i]
            #     painted_blocks[i] = painted_blocks[i + 1]  # 255 是白色
            #     painted_blocks[i + 1] = temp
            painted_blocks[i][:] = 255  # 255 是白色
            pass
    return painted_blocks


def concatenate_blocks(blocks1, blocks2):
    # 将两个数组的分割块交替拼接
    # concatenated_blocks = [blocks1[i // 2] if i % 2 == 0 else blocks2[i // 2] for i in range(len(blocks1) * 2)]
    concatenated_blocks = blocks1 + blocks2
    # 水平拼接得到最后的图像
    final_image = np.hstack(concatenated_blocks)
    return final_image


def resize_image(image, target_width=1080):
    # 获取图像的原始宽度和高度
    original_width, original_height = image.shape[1], image.shape[0]

    # 计算新的高度，以保持宽高比不变
    new_height = int((target_width / original_width) * original_height)

    # 使用cv2.resize放大图像
    resized_image = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_LINEAR)

    return resized_image


# 读取图片
img = cv2.imread('tests/img_115_(1).png')

img = resize_image(img, 720)

# 获取原图的尺寸
height, width, _ = img.shape

# 创建两个空白图像，用于存储分离出来的图像
image1 = np.zeros((height, width, 3), dtype=np.uint8)
image2 = np.zeros((height, width, 3), dtype=np.uint8)

# 随机生成一个0到1之间的数，用于分离原图的颜色值
factor = np.random.random((height, width, 1))

# 将原图的颜色值分离到两个图像中
image1_s = (img * factor).astype(np.uint8)
image2_s = (img * (1 - factor)).astype(np.uint8)

# #
# # # 拼接得到最后的图像
# final_img = concatenate_blocks(image1_s, image2_s)

TwoPFastDtwSiftImpl.draw_matches(0, image1_s, image2_s)

# 显示/保存处理后的图片
cv2.imshow('Processed Image', image1_s)
cv2.waitKey(0)
cv2.imshow('Processed Image', image2_s)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 或者保存图片
# cv2.imwrite('output.jpg', final_img)
