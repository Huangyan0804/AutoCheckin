#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from PIL import Image

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Upgrade-Insecure-Requests': '1',
}


def login():
    # 验证码地址
    code_url = 'https://passport2.chaoxing.com/num/code?1583831609442'
    login_url = 'https://passport2.chaoxing.com/login?refer=http%3A%2F%2Fi.mooc.chaoxing.com'
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.122 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'passport2.chaoxing.com',
        'Referer': 'https://passport2.chaoxing.com/login?fid=2182&refer=http://i.mooc.chaoxing.com',
        'Origin': 'https://passport2.chaoxing.com',

    }
    login_data = {
        'refer_0x001': 'http%3A%2F%2Fi.mooc.chaoxing.com',
        'pid': '-1',
        'pidName': '',
        'fid': '2182',
        'fidName': '电子科技大学中山学院',
        'allowJoin': '0',
        'isCheckNumCode': '1',
        'f': '0',
        'productid': '',
        't': 'true',
        'uname': 'gg48@qq.com',
        'password': '',  # base64加密
        'numcode': '',
        'verCode': '',
    }
    r_session = requests.session()
    response = r_session.get(url=code_url, headers=login_headers)
    with open('code_img.png', 'wb') as f:
        f.write(response.content)
    Image.open('code_img.png').show()
    numcode = input("请输入验证码：")
    login_data['numcode'] = str(numcode)
    response = r_session.post(url=login_url, headers=login_headers, data=login_data)
    # print(response.text)
    test_url = 'http://i.mooc.chaoxing.com/space/index?t=1583831617509'
    response = r_session.get(url=test_url, headers=header)
    # print(response.text)


def main():
    login()


if __name__ == '__main__':
    main()
