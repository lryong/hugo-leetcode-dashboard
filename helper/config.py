'''
@Author: KivenChen
@Date: 2019-04-22
@LastEditTime: 2019-05-05
'''
import json
import os


class Config:
    '''
    获取配置信息并储存至 `config.json`
    '''
    def __init__(self):
        self.data = self.__getConfig()

    def __getConfig(self):
        path = os.path.join(os.path.abspath(os.path.join(__file__, "../..")),
                            'config.json')
        if not os.path.exists(path):
            username = input('请输入您的用户名: ')
            password = input('请输入您的密码: ')
            outputDir = input('请选择您要输出的目录: ')
            data = dict(username=username,
                        password=password,
                        outputDir=outputDir,
                        timeInterval=0.1)
            with open(path, 'w') as f:
                json.dump(data, f)
            return data
        else:
            with open(path, 'r') as f:
                return json.load(f)

    def __getData(self, item):
        return self.data.get(item) if self.data else None

    @property
    def username(self):
        return self.__getData('username')

    @property
    def password(self):
        return self.__getData('password')

    @property
    def outputDir(self):
        return self.__getData('outputDir')

    @property
    def timeInterval(self):
        return self.__getData('timeInterval') or 0.1


config = Config()
