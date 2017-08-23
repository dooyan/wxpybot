# -*- coding:utf-8 -*-

import json
import socket
import logging
import urllib.request

socket.setdefaulttimeout(60)
# POST /api.php?cmd=chatCallback HTTP/1.1
# User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36
# Host: m.mengbaotao.com
# Accept: */*
# Cookie: 
# Content-Length: 70
# Content-Type: application/x-www-form-urlencoded

# msg=%E4%B9%88%E4%B9%88%E5%93%92&channelid=2001&openid=8643233529881511
# HTTP/1.1 200 OK
# Server: nginx/1.2.6
# Date: Wed, 12 Apr 2017 01:08:01 GMT
# Content-Type: text/html; charset=utf-8
# Transfer-Encoding: chunked
# Connection: keep-alive
# X-Powered-By: PHP/5.3.17
# Cache-Control: no-cache, no-store, max-age=0, must-revalidate
# Expires: Mon, 26 Jul 1997 05:00:00 GMT
# Pragma: no-cache

# 1eb
# {"data":{"birthday":"0","intent_type":"3","nick":"\u98de\u5929\u86cb\u86cb","npc_nick":"\u841d\u535c\u4e1d","npcnick":"\u841d\u535c\u4e1d","occupation":"\u5973\u4ec6","race":"\u706b\u661f\u4eba","rule_relate":"100","sceneid":"0","sleeptime":"3000"},"duration":0,"openid":"8643233529881511","ref":"","ret_message":"\u77ee\u6cb9\uff0c\u597d\u8212\u670d~\u98de\u5929\u86cb\u86cb\u8981\u662f\u6bcf\u5929\u90fd\u6765\u7ed9\u6211\u4e00\u4e2a\u543b\u5c31\u597d\u5566\uff01","ruleid":26148,"type":1}
# 0

#coding=utf8
 
def blacklist(retstr):
    if not retstr:
        return retstr
    if retstr.find(u'加速升级') >= 0 and retstr.find(u'加速等级') >= 0:
        retstr = u'呵呵，我不会答'
    return retstr


def say(usrid, msgstring):

    if len(usrid) <= 0:
        usrid = '8643233529881511'
    httpClient = None
    retstr = '萌萌还没睡醒哦'
    returl = None
    try:
        import requests

        #params = urllib.parse.urlencode({'msg': msgstring.encode('utf8', errors='ignore'), 'channelid': 2001, 'openid':usrid})
        params = {'msg': msgstring.encode('utf8', errors='ignore'), 'channelid': 2001, 'openid': usrid}
        headers = { "Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}

        mbburl = 'http://m.mengbaotao.com/api.php?cmd=chatCallback'

        req = requests.post(mbburl, data=params, headers=headers)
        backstr = req.text
        print(backstr)

        jsobj = json.loads(backstr)
        retstr = jsobj['ret_message']
        if len(jsobj['ref']) > 0:
            returl = jsobj['ref']
    except Exception as e:
        print(e)

    retstr = blacklist(retstr)
    return retstr, returl

def onmessage(msg):
    if not msg.type == 'Text':  # 只处理文本
        return
    if msg.text.startswith('##'):
        print(msg.sender.puid)
        retstr = say(msg.sender.puid, msg.text[2:])
        msg.reply(retstr[0])
        if retstr[1]:
            import os
            import requests
            pngcont = requests.get(retstr[1])
            pngfile = os.path.split(retstr[1])[1]
            f = open(pngfile, 'wb')
            f.write(pngcont.content)
            f.close()
            msg.reply_image(pngfile)
            os.remove(pngfile)

if __name__ == '__main__':
    str = say(u'864323352988151a', u'美女图')
    print(str)
    import requests
    bnpcc = requests.get(str[1])
    import os
    f = open(os.path.split(str[1])[1], 'wb')
    f.write(bnpcc.content)
    f.close()
    print(bnpcc)
    str = say(u'864323352988151a', u'jiang笑话')
    print(str)
    print('end')
