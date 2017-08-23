# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, '../')

import logging
# from utils.wxplugins import *

admins = ['贾振']

funcrouter = ['！插件加载']

def plugin_remote(msg, ttext):
    cmdret = ''
    try:
        cmdret = ttext[2:]
        if ttext.startswith('加载'):
            msg.bot.plugins_plug(cmdret)
            cmdret += ' 成功'
        if ttext.startswith('卸载'):
            msg.bot.plugins_unplug(cmdret)
            cmdret += ' 成功'
        if ttext.startswith('列表'):
            cmdret = '正在加载的插件：\r\n' + '\r\n'.join(msg.bot.plugins_list())
    except Exception as e:
        import traceback
        msg.reply('操作错误：%s\r\n%s' % (str(repr(e)), traceback.format_exc()))
        return
    msg.reply('%s %s' % (ttext[:2], cmdret))

def onmessage(msg):
    # logging.debug('msgplugin admin %s' % msg.type)
    if not msg.type == 'Text':
        return

    if not msg.sender.name in admins:
        return

    if msg.text.startswith('！插件'):
        plugin_remote(msg, msg.text[3:])
        return

    #msg.reply('无法解释：%s' % str(msg.text))

