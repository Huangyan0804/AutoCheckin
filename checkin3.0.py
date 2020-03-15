#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import quote
import http.cookiejar as HC
from PIL import Image

"""
    ！！！支持普通签到，手势签到，二维码签到
    学习通自动签到，针对早起不能学生，需要自行提供参数
    目前已知cookie的有效时间至少为1天
    登录方式：二维码登录，自动保存cookie
    因为匆忙制作的签到脚本，我的身体已经菠萝菠萝哒
    -----------------------------------
    需要修改的地方有：
    课程参数：
    course_list = [
        {
            'name':  # 你的姓名
            'url':  # 课程的任务页面/活动首页
            'course_name':  # 课程名称，可不填
        }
    ]
    
"""

# 需要签到的课程列表
course_list = [
    {
        'name': "",  # 姓名
        'url': '',
        'course_name': ''
    }
]

post_data = {
    'name': None,  # 姓名
    'puid': None,
    'courseId': None,  # 课程id
    'classId': None,  # 班级id
    'fid': None,  # 学校id
    'activeId': None,  # 无需填写
}

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Upgrade-Insecure-Requests': '1',
}

r_session = requests.session()


def save_html(text, filename):
    """保存html文件"""
    with open('%s.html' % filename, 'x') as f:
        f.write(text)
        print('文件%s.html已保存' % filename)


def check_is_login():
    """
    检测是否登录成功, 返回bool
    """
    request_url = 'http://i.mooc.chaoxing.com/space/'
    # print(request_url)
    response = r_session.get(url=request_url, headers=header)
    b_soup = BeautifulSoup(response.text, 'html.parser')
    title = b_soup.title.string
    if title == '用户登录':
        return False
    else:
        return True


def get_login_status(login_headers, login_data):
    """
    获取登录信息并转换成字典
    二维码未扫描返回:{"mes":"未登录","type":"3","status":false}
    二维码扫描未登录返回:{"uid":"","nickname":"","mes":"已扫描","type":"4","status":false}
    二维码扫描且登录返回: {"mes":"验证通过","status":true}
    二维码过期: {"mes":"二维码已失效","type":"2","status":false}
    二维码扫描取消登录： {"mes":"用户手机端取消登录","type":"6","status":false}
    """
    check_url = "http://passport2.chaoxing.com/getauthstatus"
    response = r_session.post(url=check_url, headers=login_headers, data=login_data)
    text = response.text
    text = text.replace('true', 'True')
    text = text.replace('false', 'False')
    dic = eval(text)
    return dic


def get_login_code(login_headers):
    login_url = 'http://passport2.chaoxing.com/cloudscanlogin?' \
                'mobiletip=%e7%94%b5%e8%84%91%e7%ab%af%e7%99%bb%e5%bd%95%e7%a1%ae%e8%ae%a4' \
                '&pcrefer=http://i.chaoxing.com'
    response = r_session.get(url=login_url, headers=login_headers)
    text = response.text
    b_soup = BeautifulSoup(text, 'html.parser')
    uuid = b_soup.find_all('input', id='uuid')[0]['value']
    enc = b_soup.find_all('input', id='enc')[0]['value']
    login_data = {'uuid': uuid, 'enc': enc}
    scanning_url = "http://passport2.chaoxing.com/createqr?uuid=" + uuid \
                   + "&xxtrefer=&type=1&mobiletip=%E7%94%B5%E8%84%91%E7%AB%AF%E7%99%BB%E5%BD%95%E7%A1%AE%E8%AE%A4"
    print("二维码扫描网址：" + scanning_url)
    response = r_session.get(url=scanning_url, headers=login_headers)
    try:
        with open('code_img.png', 'xb') as f:
            f.write(response.content)
    except:
        with open('code_img.png', 'wb') as f:
            f.write(response.content)
    Image.open('code_img.png').show()
    # qrcode_terminal.draw(scanning_url)
    input("扫描登陆后请确认(y):")
    return get_login_status(login_headers, login_data)


def re_login(login_headers):
    login_status = get_login_code(login_headers)
    if login_status['status']:
        print("登录成功")
        r_session.cookies.save()
    else:
        if login_status['type'] == '4':
            print("登录失败," + login_status['mes'] + "却未登录")
        else:
            print("登录失败," + login_status['mes'])


def login():
    """登陆函数"""
    # 登录地址
    login_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.122 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'passport2.chaoxing.com',
        'Referer': 'https://passport2.chaoxing.com/login?fid=2182&refer=http://i.mooc.chaoxing.com',
        'Origin': 'https://passport2.chaoxing.com',
    }
    r_session.cookies = HC.LWPCookieJar(filename='cookies')

    try:
        r_session.cookies.load(ignore_discard=True)
        if not check_is_login():
            print('cookie信息已过期，请重新登录')
            re_login(login_headers)
        else:
            print('已登录')
    except:
        print('请登录')
        re_login(login_headers)

active_list = []


def get_post_data(text):
    b_soup = BeautifulSoup(text, 'html.parser')
    post_data['puid'] = b_soup.find_all('input', id='puid')[0]['value']
    post_data['courseId'] = b_soup.find_all('input', id='courseId')[0]['value']
    post_data['classId'] = b_soup.find_all('input', id='classId')[0]['value']
    post_data['fid'] = b_soup.find_all('input', id='fid')[0]['value']


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


def normal_check(base_url, post_data):
    """普通签到"""
    args = "/widget/sign/pcStuSignController/preSign?" \
           + "activeId=" + post_data['activeId'] \
           + "&classId=" + post_data['classId'] \
           + "&fid=" + post_data['fid'] \
           + "&courseId=" + post_data['courseId']
    response = r_session.get(url=base_url + args, headers=header)
    return response


def hand_check(base_url, post_data):
    """手势签到"""
    args = "/widget/sign/pcStuSignController/signIn?" \
           + "&courseId=" + post_data['courseId'] \
           + "&classId=" + post_data['classId'] \
           + "&activeId=" + post_data['activeId']
    response = r_session.get(url=base_url + args, headers=header)
    return response


def qcode_check(base_url, post_data):
    """二维码签到"""
    args = "/pptSign/stuSignajax?" \
           + "name=" + post_data['name'] \
           + "&activeId=" + post_data['activeId'] \
           + "&uid=" + post_data['puid'] \
           + "&clientip=&useragent=&latitude=-1&longitude=-1" \
           + "&fid=" + post_data['fid'] + "&appType=15"
    response = r_session.get(url=base_url + args, headers=header)
    return response


def check_in():
    """post 签到"""
    if not active_list:
        print("没有签到任务或者登录失败")
        return
    # 循环签到各个任务
    for active_id in active_list:
        post_data['activeId'] = active_id
        base_url = 'https://mobilelearn.chaoxing.com'
        # 打开签到页
        response = normal_check(base_url, post_data)
        if re.findall(r'签到成功', response.text):
            print("==========>%s已签到成功" % active_id)
        else:
            if re.findall(r'手势图案', response.text):
                # 手势签到
                response = hand_check(base_url, post_data)
                if re.findall(r'签到成功', response.text):
                    print("==========>%s手势签到成功" % active_id)
            elif re.findall(r'手机扫码', response.text):
                # 二维码签到
                response = qcode_check(base_url, post_data)
                if re.findall(r'success', response.text):
                    print("==========>%s二维码签到成功" % active_id)
            else:
                print('暂不支持的签到类型')
        # print("==========>%s签到失败" % active_id)
        # save_html(response.text, active_id)
        time.sleep(3)


def open_course_page(course):
    """打开课程活动页"""
    print('正在检查%s课程签到任务' % course['course_name'])
    current_time = str(time.strftime("%m-%d %H:%M:%S", time.localtime()))
    request_url = course['url']
    print(request_url)
    response = r_session.get(url=request_url, headers=header)
    text = response.text
    # save_html(text, current_time)
    active_list.clear()  # 获得id前清空
    get_post_data(text)  # 获取post_data
    get_active_id(text)  # 获取签到任务
    check_in()  # 签到


def main():
    # login()  # 登陆函数，根据需要自行调用
    for course in course_list:
        # 遍历课程检查是否需要签到
        open_course_page(course)
        print('-' * 50)
        time.sleep(5)


if __name__ == '__main__':
    main()
