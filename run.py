# -*- coding: utf-8 -*-
'''
@Author: KivenChen
@Date: 2019-04-23
@LastEditTime: 2019-05-02
'''
from helper.main import Main

if __name__ == "__main__":
    while True:
        print('欢迎使用 LeetCode_Helper, 请选择: ')
        print('1. 更新')
        print('2. 重建')
        print('q. 退出')
        key = input()
        if key == 'q':
            break
        elif key == '1':
            Main().update()
            break
        elif key == '2':
            Main().rebuild()
            break
        else:
            print('请重新选择！')
print("thanks for using")
