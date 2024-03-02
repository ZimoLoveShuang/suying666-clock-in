import datetime
import os
import re
import sys
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# server酱key
key = ''
# 账号
email = ''
# 密码
passwd = ''
# session
session = requests.session()


# 登陆
def login(host):
    parsed_url = urlparse(host)
    # 1. 做浏览器认证
    headers = {
        'host': parsed_url.netloc,
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    res = session.get(url=host, headers=headers)
    # print(res.text)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    if 'ge_ua_p' in cookie:
        time.sleep(5)
        print(cookie)
        n = cookie['ge_ua_p']
        s = re.search('var nonce = \d+;', res.text)
        nonce = int(s[0][s[0].rindex('=') + 1:-1])
        print(nonce)
        a = 0
        for o in range(len(n)):
            d = n[o]
            if d.isalpha() or d.isdigit():
                a += ord(d) * (nonce + o)
        print('a', a)
        headers = {
            'Host': parsed_url.netloc,
            'Connection': 'keep-alive',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-platform': '"Windows"',
            'X-GE-UA-Step': 'prev',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': host,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': host + '/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'ge_ua_p=' + n,
        }
        res = session.post(
            url=res.url,
            data={'sum': a, 'nonce': nonce},
            headers=headers
        )
        print(res.text)

    # 2. 登录
    url = '{}/auth/login'.format(host)
    params = {
        'email': email,
        'passwd': passwd,
        'code': ''
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': url,
        'Referer': '{}/auth/login'.format(url),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = session.post(url=url, headers=headers, data=params, timeout=30)
    msg = res.json()['msg']
    print(msg)
    ret = ''
    if msg == '登录成功':
        # 登陆成功之后，去更新hosts.txt
        del headers['Content-Type']
        headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        html = session.get('{}/user'.format(host), headers=headers, timeout=30).text
        soup = BeautifulSoup(html, 'lxml')
        hosts = set()
        for i in soup.find_all('h6'):
            a = i.find('a', text=re.compile('http.*'))
            if (a) and (re.search(r'[\u4e00-\u9fa5]', a.text) is None) and ('美区苹果账号购买地址' not in a.text):
                hosts.add(a.text)
        with open('hosts.txt', 'w', encoding='utf-8') as f:
            for i in hosts:
                f.write('{}\n'.format(i))
        print('更新hosts.txt完成')
        # 获取登陆信息
        statistics = soup.find_all(class_='card card-statistic-2')
        for i in statistics:
            for j in i.text.split('\n'):
                if len(j) > 1:
                    a = j.replace('\n', '').replace('\r', '').replace('升级套餐', '').strip()
                    ret += a + ' '
            ret += '\n\n'
        return ret
    else:
        raise Exception(msg)


# 速鹰666签到领流量
def clockIn(host):
    url = '{}/user/checkin'.format(host)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '0',
        'Origin': host,
        'Referer': '{}/user'.format(host),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = session.post(url=url, headers=headers, timeout=30)
    json = res.json()
    print(json)
    return json


def sendMessage(msg):
    # print(msg)
    if key:
        res = requests.post(
            url='https://sc.ftqq.com/' + key + '.send',
            data={
                'title': '速鹰666自动签到结果通知',
                'desp': msg
            },
            timeout=30
        )
        # print(res.text)


def main_handler(event, context):
    hosts = [i.strip() for i in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    for host in hosts:
        try:
            print('try', host)
            lmsg = login(host)
            json = clockIn(host)
            msg = json['msg']
            ret = json['ret']
            # print(lmsg + '今日签到 ' + msg)
            if ret == 1:
                sendMessage(lmsg + '今日签到 ' + msg)
                break
            else:
                break
        except Exception as e:
            print(e)
    # 当没有更新hosts时，保留原有的hosts
    hosts2 = [i.strip() for i in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    if not hosts2:
        with open('hosts.txt', 'w', encoding='utf-8') as f:
            for i in hosts:
                f.write('{}\n'.format(i))



if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) != 4:
        print('usage:python3 {} "email" "passwd" "key"'.format(sys.argv[0]))
        exit()
    print(datetime.datetime.now())
    email, passwd, key = sys.argv[1:]
    if (not len(email)) or (not len(passwd)):
        print('email or passwd is null')
        exit()
    main_handler({}, {})
