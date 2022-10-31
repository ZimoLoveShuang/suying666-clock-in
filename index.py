import os
import re
import sys

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
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = session.post(url=url, headers=headers, data=params, timeout=10)
    msg = res.json()['msg']
    print(msg)
    if msg == '登录成功':
        # 登陆成功之后，去更新hosts.txt
        del headers['Content-Type']
        html = session.get('{}/user'.format(host), headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        # for i in soup.find_all(text=re.compile('<h5 id=".*"><a class="reference-link" .*</a></h5>')):
        hosts = set()
        for i in soup.find_all('h5'):
            a = i.find('a', text=re.compile('http.*'))
            if a:
                hosts.add(a.text)
        with open('hosts.txt', 'w', encoding='utf-8') as f:
            for i in hosts:
                f.write('{}\n'.format(i))


# 速鹰666签到领流量
def clockIn(host):
    url = '{}/user/checkin'.format(host)
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': url,
        'Referer': '{}/user'.format(host),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    res = session.post(url=url, headers=headers)
    json = res.json()
    print(json)
    return json


def sendMessage(msg):
    url = 'https://sc.ftqq.com/' + key + '.send?text=' + msg;
    res = requests.get(url)
    print(res.json())


def main_handler(event, context):
    hosts = [i.strip() for i in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    for host in hosts:
        try:
            print('try', host)
            login(host)
            json = clockIn(host)
            msg = json['msg']
            ret = json['ret']
            if ret == 1:
                sendMessage(msg)
                break
            else:
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) != 4:
        print('usage:python3 {} "email" "passwd" "key"'.format(sys.argv[0]))
        exit()
    print(sys.argv[1:])
    email, passwd, key = sys.argv[1:]
    if (not len(email)) or (not len(passwd)):
        print('email or passwd is null')
        exit()
    main_handler({}, {})
