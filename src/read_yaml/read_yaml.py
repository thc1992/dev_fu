import json

import yaml
import os

yam_path = os.path.dirname(os.path.abspath(__file__)) + '/../common/config.yaml'
yam_path2 = os.path.dirname(os.path.abspath(__file__)) + '/../common/token.yaml'

class Read_yaml(object):
    def yaml_show(self, key):
        try:
            with open(yam_path, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if key in data.keys():
                    return data[key]

        except:
            return None

    # 将token值写入token.yaml文件中
    def write_yaml(self, key_vule):
        with open(yam_path2, 'w', encoding='utf-8') as f:
            yaml.dump(key_vule, f)

    # 读取token.yaml文件中
    def yaml_show_token(self, key):
        try:
            with open(yam_path2, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if key in data.keys():
                    return data[key]
        except:
            return None


if __name__ == '__main__':
    dtalk = Read_yaml().yaml_show_token('access_token')
    # json_str = {'access_token': 'niaho'}
    # Read_yaml().write_yaml(json_str)
    print(dtalk)
