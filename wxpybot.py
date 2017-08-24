# -*- coding:utf-8 -*-

import os
import sys
import time
import logging
import threading
import utils.logfile as logfile
import utils.itchatpatch as itchatpatch
from wxpy import *
from utils.wxpyconf import *
from utils.wxplugins import *

# 初始化日志
logfile.console_and_logfile('./logs/testrslog')


# 初始化插件, 由于初始化bot需要插件回掉，插件回掉要引用bot，无法两全
addPath(os.path.join(os.path.split(__file__)[0], 'plugin'))
initplugins = ['admin', 'mbaotaochat', 'heartbeat', 'picsaver']
for iplugname in initplugins:
    modImport(iplugname)
    modCall(iplugname, 'onPlug', kargs={'bot':None})


def qr_callback(uuid, status, qrcode):
    logging.debug('qr_callback uuid=%s status=%s qrcode=%d' % (uuid, status, len(qrcode)))
    fname = 'pnstart.login.png'
    with open(fname, 'wb') as f:
        f.write(qrcode)
    os.system('mspaint %s' % fname)
    pass


# 登陆回掉
def login_callback():
    try:
        modCallAlls('onlogin')
    except:
        pass
    print('login_callback')


# 登出回掉
def logout_callback():
    try:
        modCallAlls('onlogout')
    except:
        pass
    print('logout_callback')


# 初始化机器人
bot = Bot(  cache_path=wxbot_loginsession_file,
            qr_path=wxbot_loginqr_file,
            # qr_callback=qr_callback,
            login_callback=login_callback,
            logout_callback=logout_callback)

bot.enable_puid(wxbot_puid_file)


# 初始化机器人插件
def plugins_plug(name):
    try:
        modImport(name)
        modCall(name, 'onPlug', kargs={'bot': bot})
        logging.info('plugins %s onPlug finish' % name)
    except Exception as e:
        import traceback
        logging.info('plugins onPlug：%s\r\n%s' % (str(repr(e)), traceback.format_exc()))
        bot.file_helper.send('plugins onPlug failed \r\n %s' % str(repr(e)))
        return


def plugins_unplug(name):
    try:
        modCall(name, 'onUnplug', kargs={'bot': bot})
        modRemove(name)
        logging.info('plugins %s onUnplug finish' % name)
    except Exception as e:
        import traceback
        logging.info('plugins onUnplug：%s\r\n%s' % (str(repr(e)), traceback.format_exc()))
        bot.file_helper.send('plugins onUnplug failed \r\n %s' % str(repr(e)))
        return

bot.plugins_plug = plugins_plug
bot.plugins_unplug = plugins_unplug
bot.plugins_list = modList


intervaltimer = None


def Intervalpluginscall(botcore):
    logging.debug('Intervalpluginscall check %d' % time.time())
    try:
        modCallAlls('onInterval', bot=botcore)
    except:
        pass

    global intervaltimer
    if not intervaltimer:
        del intervaltimer
    intervaltimer = threading.Timer(60.0*5, Intervalpluginscall, kwargs={'botcore': botcore})
    intervaltimer.start()


intervaltimer = threading.Timer(60.0*5, Intervalpluginscall, kwargs={'botcore': bot})
intervaltimer.start()

# 所有消息回掉
anymsgtype = [TEXT,MAP,CARD,NOTE,SHARING,PICTURE,RECORDING,ATTACHMENT,VIDEO,FRIENDS ]

@bot.register(msg_types=anymsgtype, except_self=False)  # , run_async=False
def message_all_plugins(msg):
    try:
        modCallAlls('onmessage', msg=msg)
    except:
        pass

bot.join()

if intervaltimer:
    intervaltimer.cancel()
