# -*- coding:utf-8 -*-

import sys
sys.path.insert(0, '../')

import os
import logging
from bypy import ByPy

admins = ['贾振']


base_remote_dirname = 'wxpybot'

def bdy_list_interal(bypy, remotepath):
    bypy.list(remotepath)
    retjson = bypy.jsonq[len(bypy.jsonq) - 1]
    return retjson['list']

def bdy_makedir_interal(bypy, remotepath):
    bypy.mkdir(remotepath)
    retjson = bypy.jsonq[len(bypy.jsonq) - 1]
    return retjson['list']

def bdy_initdir(bypy):
    dirlist = bdy_list_interal(bypy, '')

    bfinddir = False
    for idir in dirlist:
        if idir['isdir'] == 0:
            continue

        if idir['path'] == '/apps/bypy/' + base_remote_dirname:
            bfinddir = True
            break

    if not bfinddir:
        logging.debug('bdy_makedir %s' % base_remote_dirname)
        bdy_makedir_interal(bypy, base_remote_dirname)


def bdy_upload(bypy, localfile):
    if not os.path.isfile(localfile):
        return ['没找到', localfile]
    if localfile.find('\\') >= 0 or localfile.find('/') >= 0:
        filename = os.path.split(localfile)[1]
    else:
        filename = localfile
    bypy.upload(localfile, '%s/%s' % (base_remote_dirname, filename))
    return ['上传完成', filename]

def bdy_download(bypy, filename, localdir=None):
    if not localdir or len(localdir) <= 0 or localdir=='.':
        localdir = os.path.split(__file__)[0]
        localdir = os.path.split(localdir)[0]
        localdir = os.path.join(localdir, 'baiduyun')

    os.makedirs(localdir, exist_ok=True)

    downtofile = os.path.join(localdir, filename)
    # print('/apps/bypy/%s/%s' % (base_remote_dirname, filename))
    # print(downtofile)

    bypy.downfile('%s/%s' % (base_remote_dirname, filename), downtofile)

def local_list(localdir):
    alist = os.listdir(localdir)
    if len(alist) > 30:
        alist = alist[:30]
    return alist

def local_run(localcmd):
    from subprocess import Popen, PIPE
    p = Popen(localcmd, shell=True, stdout=PIPE)
    out = p.stdout.readlines()
    for i in range(len(out)):
        if type(out[i]) == type(b''):
            out[i] = out[i].decode('gbk', errors='ignore')
    return out

def plugin_remote(msg, ttext):
    cmdret = ''
    try:
        cmdret = ttext[2:]
        if ttext.startswith('上传'):
            bp = ByPy()
            bdy_initdir(bp)
            cmdret = '本地文件：\r\n' + '\r\n'.join(bdy_upload(bp, ttext[2:]))
            cmdret += ' 成功'
        if ttext.startswith('下载'):
            cmdret += ' 暂不支持'
        if ttext.startswith('列表'):
            cmdret = '本地文件：\r\n' + '\r\n'.join(local_list(ttext[2:]))
        if ttext.startswith('命令'):
            cmdret = '本地命令：\r\n' + ' '.join(local_run(ttext[2:]))
    except Exception as e:
        import traceback
        msg.reply('操作错误：%s\r\n%s' % (str(repr(e)), traceback.format_exc()))
        cmdret = str(repr(e))

    if len(cmdret) > 0:
        msg.reply('%s %s' % (ttext[:2], cmdret))


def onmessage(msg):
    # logging.debug('msgplugin admin %s' % msg.type)
    if not msg.type == 'Text':
        return

    if not msg.sender.name in admins:
        return

    if msg.text.startswith('！云盘'):
        plugin_remote(msg, msg.text[3:])
        return

    #msg.reply('无法解释：%s' % str(msg.text))

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%H:%M:%S',  # 时间
    )

    bp = ByPy()
    bdy_initdir(bp)

    localfile = 'C:\\Python3\\python.exe'
    #bdy_upload(bp, localfile)

    # bdy_download(bp, 'python.exe')

    print(local_run('dir'))
    pass
