import requests

# server酱key
key = ''
# 账号
email = ''
# 密码
passwd = ''
# session
session = requests.session()
host = 'suying999.net'


# 登陆
def login():
    url = 'https://{host}/auth/login'.format(host=host)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': host,
        'Origin': 'http://' + host,
        'Referer': 'https://{host}/auth/login'.format(host=host),
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest',
    }
    params = {
        'email': email,
        'passwd': passwd,
        'code': ''
    }

    res = session.post(url=url, headers=headers, data=params)
    msg = res.json()['msg']
    return msg


# 速鹰666签到领流量
def clockIn():
    url = 'https://{host}/user/checkin'.format(host=host)
    headers = {
        'Host': host,
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://' + host,
        'Referer': 'https://{host}/user'.format(host=host),
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
    msg = login()
    print(msg)
    json = clockIn()
    msg = json['msg']
    print(msg)
    sendMessage(msg)


if __name__ == '__main__':
    main_handler({}, {})
