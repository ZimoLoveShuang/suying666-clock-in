# suying666-clock-in

速鹰666自动签到领流量，配合github actions使用

# 使用
1. fork此仓库，必须在github上fork
2. 点击Settings->Secrets->Actions->New repository secret，依次配置`EMAIL`、`KEY`、`PASSWD`
    - EMAIL 是suying666的账号
    - PASSWD 是suying666的密码
    - KEY是server酱的key，获取key参考[server酱官方说明](http://sc.ftqq.com/3.version)
3. UTC时间的每天01:00分（北京时间：09:00，并不准时），github actions会自动帮助您签到领取流量，如果您配置了server酱的key的话，您将收到微信消息通知
4. enjoy it!!!

# 特性

1. 每次登陆成功后，自动更新hosts.txt，避免因为host被墙，而自动签到失败
2. 完全免费，不需要服务器，与云函数