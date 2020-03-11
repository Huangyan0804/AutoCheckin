#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
from PIL import Image

"""
    ！！！仅支持普通签到
    学习通自动签到，针对早起不能学生，需要自行提供参数和cookie
    目前未知cookie的有效时间
    小白勿用

    因为匆忙制作的签到脚本，我的身体已经菠萝菠萝哒
    -----------------------------------
    需要修改的地方有：
    课程参数：
    course_list = [
        {
            'courseId':  # 课程号
            'classId':  # 班级号,
            'course_name':  # 课程名称，可以为空，用于输出日志
        }
    ]
    登陆参数：
    login_data {
        uname:  # 用户名
        password:  #自行base64加密
    }
    可选参数：
    header {
        Cookie： # Cookie免登陆
    }
"""

# 需要签到的课程列表
course_list = [
    {
        # 本人的test
        'courseId': '210575187',
        'classId': '21697074',
        'course_name': 'test'
    },
    {
        # 本人的java课程
        'courseId': '210205345',
        'classId': '21276854',
        'course_name': 'java'
    },
    {
        # 本人的Web课程
        'courseId': '203426623',
        'classId': '14232535',
        'course_name': 'web'
    }
]

# 登陆用数据
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
    'uname': '',  # 用户名
    'password': '',  # base64加密
    'numcode': '',
    'verCode': '',
}

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Upgrade-Insecure-Requests': '1',
    # 'Cookie': '',  # 可选参数，免登陆
}

r_session = requests.session()


def save_html(text, filename):
    """保存html文件"""
    with open('%s.html' % filename, 'x') as f:
        f.write(text)
        print('文件%s.html已保存' % filename)


def login():
    """登陆函数"""
    # 验证码地址
    code_url = 'https://passport2.chaoxing.com/num/code?1583831609442'
    # 登录地址
    login_url = 'https://passport2.chaoxing.com/login?refer=http%3A%2F%2Fi.mooc.chaoxing.com'
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.122 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'passport2.chaoxing.com',
        'Referer': 'https://passport2.chaoxing.com/login?fid=2182&refer=http://i.mooc.chaoxing.com',
        'Origin': 'https://passport2.chaoxing.com',
    }

    response = r_session.get(url=code_url, headers=login_headers)
    with open('code_img.png', 'wb') as f:
        f.write(response.content)
    Image.open('code_img.png').show()
    numcode = input("请输入验证码：")
    login_data['numcode'] = str(numcode)
    # 登录
    response = r_session.post(url=login_url, headers=login_headers, data=login_data)


active_list = []


def get_active_id(text):
    """获取签到活动id"""
    b_soup = BeautifulSoup(text, 'html.parser')
    start_list = b_soup.find_all('div', id='startList')
    for x in start_list:
        y = x.find_all('div')
        for i in range(len(y)):
            try:
                rawid = y[i]['onclick']
                active_id = re.findall(r'activeDetail\((\d+),.*?\)', rawid)[0]
                print(active_id)
                active_list.append(active_id)
            except Exception as ret:
                pass


def check_in(course):
    """post 签到"""
    post_data = {
        'courseId': None,  # 课程id
        'classId': None,  # 班级id
        'fid': '2182',  # 学校id
        'activeId': None  # 无需填写
    }

    if not active_list:
        print("没有签到任务或者登录失败")
    for active_id in active_list:
        post_data['activeId'] = active_id
        post_data['courseId'] = course['courseId']
        post_data['classId'] = course['classId']
        base_url = 'https://mobilelearn.chaoxing.com'
        args = "/widget/sign/pcStuSignController/preSign?" + \
               "activeId=" + post_data['activeId'] + "&classId=" + post_data['classId'] + "&fid=" \
               + post_data['fid'] + "&courseId=" + post_data['courseId']
        response = r_session.get(url=base_url + args, headers=header)
        # print(response.text)
        if re.findall(r'签到成功', response.text):
            print("==========>%s签到成功" % active_id)
        else:
            print("==========>%s签到失败" % active_id)
            save_html(response.text, active_id)
        time.sleep(3)


def open_course_page():
    """打开课程活动页"""
    base_url = 'https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?'

    for course in course_list:
        print('正在检查%s课程签到任务' % course['course_name'])
        current_time = str(time.strftime("%m-%d %H:%M:%S", time.localtime()))
        request_url = base_url + 'courseId=' + course['courseId'] + '&jclassId=' + course['classId']
        print(request_url)
        response = r_session.get(url=request_url, headers=header)
        text = response.text
        save_html(text, current_time)
        active_list.clear()  # 获得id前清空
        get_active_id(text)  # 获取签到任务
        check_in(course)  # 签到
        print('-'*50)
        time.sleep(5)


def main():
    # login()  # 登陆函数，根据需要自行调用
    open_course_page()


if __name__ == '__main__':
    main()
