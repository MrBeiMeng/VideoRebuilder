import json


class GlobalStorage:
    storage_map: dict = {}

    @staticmethod
    def set(key, data):
        print(f'set [{key}]={data}')
        GlobalStorage.storage_map[key] = data

    @staticmethod
    def get(key):
        return GlobalStorage.storage_map[key]

    @staticmethod
    def exist(key):
        return key in GlobalStorage.storage_map

    @staticmethod
    def dump():
        file_path = GlobalStorage.get('cache_path')
        with open(file_path, 'w') as json_file:
            json.dump(GlobalStorage.storage_map, json_file)
            print(f'Global Storage 保存至 [{file_path}]')

    @staticmethod
    def parse(file_path):
        try:
            with open(file_path, 'r') as json_file:
                GlobalStorage.storage_map = json.load(json_file)
                print(f'Global Storage 读取成功 [{file_path}]')
            GlobalStorage.storage_map['cache_path'] = file_path

        except FileNotFoundError:
            print('Warning 未找到 Global Storage ,如果是第一次运行项目，则为正常')
            pass
