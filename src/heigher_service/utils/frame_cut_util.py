import json
import os


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
