import json
import os

import os

import cv2
import json



class FrameCutUtil:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            json_path = 'src/common/crop_info.json'
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    cls._instance.crop_info = json.load(json_file)

            print(f"inited frame_cut_util = [{cls._instance.crop_info}]")
        return cls._instance

    def get_crop_info(self):
        return self.crop_info


class FrameCutUtilXiGua:
    _instance = None

    def __new__(cls, crop_info_path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            json_path = crop_info_path
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    cls._instance.crop_info = json.load(json_file)

            else:
                raise Exception('找不着！crop info，咋搞的')

            print(f"inited frame_cut_util = [{cls._instance.crop_info}]")
        return cls._instance

    def get_crop_info(self):
        return self.crop_info


class CropInfoUtils:
    def __init__(self, json_path=None):

        self.changed = False

        self.json_path = json_path or 'crop_info_madajiasijiadeqie.json'
        if not os.path.exists(self.json_path):
            with open(self.json_path, 'w') as json_file:
                json_file.write(
                    '{"x_ratio_start": 0.12265625, "y_ratio_start": 0.17777777777777778, "x_ratio_end": 0.9875, '
                    '"y_ratio_end": 0.7416666666666667}')
        with open(self.json_path, 'r') as json_file:
            self.crop_info = json.load(json_file)

        pass  # your initialization code

    @staticmethod
    def resize_image(image, target_width=1080):
        # 获取图像的原始宽度和高度
        original_width, original_height = image.shape[1], image.shape[0]

        # 计算新的高度，以保持宽高比不变
        new_height = int((target_width / original_width) * original_height)

        # 使用cv2.resize放大图像
        resized_image = cv2.resize(image, (target_width, new_height), interpolation=cv2.INTER_LINEAR)

        return resized_image

    # @staticmethod
    def get_crop_info(self, frame):
        global cropping, x_start, y_start, x_end, y_end
        cropping = False
        x_start, y_start, x_end, y_end = 0, 0, 0, 0

        def mouse_callback(event, x, y, flags, param):
            global cropping, x_start, y_start, x_end, y_end
            if event == cv2.EVENT_LBUTTONDOWN:
                x_start, y_start, cropping = x, y, True
            elif event == cv2.EVENT_MOUSEMOVE:
                if cropping:
                    x_end, y_end = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                x_end, y_end, cropping = x, y, False
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                b_frame = CropInfoUtils.resize_image(frame)
                cv2.imshow("Frame", frame)

        height, width = frame.shape[:2]

        # Load previous crop info if exists
        crop_info = self.crop_info
        x_start = int(crop_info['x_ratio_start'] * width)
        y_start = int(crop_info['y_ratio_start'] * height)
        x_end = int(crop_info['x_ratio_end'] * width)
        y_end = int(crop_info['y_ratio_end'] * height)
        cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        b_frame = CropInfoUtils.resize_image(frame)
        cv2.imshow("Frame", frame)
        cv2.setMouseCallback("Frame", mouse_callback)

        cv2.waitKey(0)
        # cv2.destroyAllWindows()

        crop_info_v2 = {
            "x_ratio_start": x_start / width,
            "y_ratio_start": y_start / height,
            "x_ratio_end": x_end / width,
            "y_ratio_end": y_end / height
        }

        for key in self.crop_info:
            if key in crop_info_v2:
                if crop_info[key] != crop_info_v2[key]:
                    print(f'Difference found: key={key}, crop_info={crop_info[key]}, crop_info_v2={crop_info_v2[key]}')
                    self.changed = True
                    break  # Break on first difference
            else:
                print(f'Key {key} not found in crop_info_v2')
                break  # Break if key not found

        if self.changed:
            self.changed = False
            # Save new crop info to JSON
            with open(self.json_path, 'w') as json_file:
                json.dump(crop_info_v2, json_file)
                print("写操作")

            self.crop_info = crop_info_v2
            print(f"更新crop_info {self.crop_info}")

        cv2.destroyAllWindows()

        return crop_info

