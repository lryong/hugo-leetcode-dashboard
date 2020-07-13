# -*- coding: utf-8 -*-
from .problems import Problems


class Main:
    '''主程序'''
    def __init__(self):
        self.problems = Problems()

    def __info(self):
        print(self.problems.info)

    def update(self):
        '''更新数据'''
        self.__info()
        self.problems.update()

    def rebuild(self):
        '''重建数据'''
        self.__info()
        self.problems.rebuild()
