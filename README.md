# suying666-clock-in

速鹰666签到领流量，配合github actions使用

# 使用
1. fork此仓库，必须在github上fork
2. 点击Settings->Secrets->Actions->New repository secret，依次配置`EMAIL`、`KEY`、`PASSWD`
    - EMAIL 是suying666的账号
    - PASSWD 是suying666的密码
    - KEY是server酱的key，获取key参考[server酱官方说明](http://sc.ftqq.com/3.version)
3. UTC时间的每天下午17:30分（不准时），github actions会自动帮助您签到领取流量，如果您配置了server酱的key的话，您将收到微信消息通知
4. enjoy it!!!

