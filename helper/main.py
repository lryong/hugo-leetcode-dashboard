'''
@Author: KivenChen
@Date: 2019-04-23
'''
from .problems import Problems
import asyncio


class Main:
    '''主程序'''
    def __init__(self):
        self.problems = Problems()

    def __info(self):
        print(self.problems.info)

    def update(self):
        '''更新数据'''
        self.__info()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.problems.update())

    def rebuild(self):
        '''重建数据'''
        self.__info()
        self.problems.clearDB()
        self.update()
