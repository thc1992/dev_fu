# encoding=utf-8
import yaml
import os

yam_path = os.path.dirname(os.path.abspath(__file__)) + '/../common/'


class Read_yaml(object):
    def yaml_show(self, key, name='config.yaml'):
        try:
            with open(yam_path + name, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if key in data.keys():
                    return data[key]

        except:
            return None

    # 将token值写入token.yaml文件中
    def write_yaml(self, key_vule, name='token.yaml'):
        with open(yam_path + name, 'w', encoding='utf-8') as f:
            yaml.dump(key_vule, f)

    def read_yaml_all(self, name='config.yaml'):
        with open(yam_path + name, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data

    def update_yaml(self, old_data, name='token.yaml'):
        with open(yam_path + name, "w", encoding="utf-8") as f:
            yaml.dump(old_data, f)


if __name__ == '__main__':
    dtalk = 'derfu365COM'
    old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
    # 修改读取的数据（k存在就修改对应值，k不存在就新增一组键值对）
    old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
    old_data['passwd'] = dtalk
    Read_yaml().update_yaml(old_data, 'token.yaml')
    # json_str = {'access_token': 'niaho'}
    # Read_yaml().write_yaml(json_str)
