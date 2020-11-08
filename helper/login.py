'''
@Author: KivenChen
@Date: 2019-04-22
@LastEditTime: 2019-05-05
'''
import requests
from .constants import LEETCODE, LOGIN, HEADERS


class Login:
    '''
    登录 LeetCode-cn, 获取 cookies 值
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__cookies = ''
        self.status = False

    def doLogin(self):
        resp = requests.get(LEETCODE, headers=HEADERS)
        # token = resp.cookies['csrftoken']
        token = ""
        headers = HEADERS.copy()
        headers.update({
            'referer': LOGIN,
            'x-csrftoken': token,
            'x-requested-with': 'XMLHttpRequest'
        })
        payload = {
            'login': self.username,
            'password': self.password,
            'csrfmiddlewaretoken': token
        }
        cookies = {'csrftoken': token}
        resp = requests.post(
            LOGIN, data=payload, headers=headers, cookies=cookies)
        if resp.status_code == 200:
            self.status = True
            self.__cookies = resp.cookies
            # user = resp.json()['form']['fields']['login']['value']
        if self.status:
            print(f'{self.username} 登录成功！')
        else:
            print('登录失败！')
            print('请检查用户名和密码！')

    @property
    def cookies(self):
        if not self.status:
            self.doLogin()
        return self.__cookies
