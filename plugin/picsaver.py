import sys
sys.path.insert(0, '../')

import os
import logging
from datetime import datetime

basepath = os.path.split(__file__)[0]
basepath = os.path.split(basepath)[0]
basepath = os.path.join(basepath, 'picsaver')
os.makedirs(basepath, exist_ok=True)

def onmessage(msg):
    # 只处理文件类型
    # logging.debug('msgplugin picsaver %s' % msg.type)
    if not msg.type in ['Picture', 'Recording', 'Video', 'Attachment']:  #
        return

    filename = '%s-%s' % (datetime.now().strftime('%Y%m%d-%H%M%S'), msg.file_name)
    logging.debug('picsaver info = %s %s %s' % (msg.sender.name, msg.file_name, msg.file_size))

    filefullpath = os.path.join(basepath, filename)

    msg.get_file(filefullpath)

    retstr = '新文件已经接收保存\r\n'
    retstr += '文件名: %s\r\n' % msg.file_name
    retstr += '文件大小: %d\r\n' % os.path.getsize(filefullpath)
    retstr += '发件人: %s\r\n' % msg.sender.name
    retstr += '文件ID: %d' % len(msg.media_id)
    msg.bot.file_helper.send(retstr)

