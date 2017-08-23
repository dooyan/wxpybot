# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, '../')

import logging

demouser = ['贾振']
def onmessage(msg):
    # logging.debug('msgplugin demo %s' % msg.type)
    if not msg.sender.name in demouser:
        return

    msg.reply('测试输出123：%s' % str(msg.text))

