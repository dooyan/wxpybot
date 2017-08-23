# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, '../')

import logging
import threading
from datetime import datetime

last_hips_datetime = datetime.now()

def onInterval(bot):
    if not bot:
        return

    global last_hips_datetime

    timepass = datetime.now() - last_hips_datetime

    if timepass.total_seconds() <= 60*60*2:
        return

    timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hips_datetime = last_hips_datetime.strftime('%Y-%m-%d %H:%M:%S')

    logging.info('onInterval = %s' % timestr)


    bot.file_helper.send('机器人心跳 = %s [%d]' % (timestr, timepass.total_seconds()))
    last_hip_time = datetime.now()