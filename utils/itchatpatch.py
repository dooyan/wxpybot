# -*- coding: utf-8 -*-
# modify 修复一些itchat内部的错误， 基于windows的python 3.4.4, 部分功能

import os
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

org_checkssl = requests.get
def nocheckverify_sslget(url, params=None, **kwargs):
    # print('nocheckverify_sslget', url)
    kwargs['verify'] = False
    return org_checkssl(url, params, **kwargs)
requests.get = nocheckverify_sslget

org_sslsesstion_request = requests.Session.request
def nocheckverify_sslsesstion_request(self, method, url,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None):
    # print('nocheckverify_sslsesstion_request', url)
    return org_sslsesstion_request(self, method, url,
            params=params, data=data, headers=headers, cookies=cookies, files=files,
            auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
            hooks=hooks, stream=stream, verify=False, cert=cert, json=json)
requests.Session.request = nocheckverify_sslsesstion_request

org_os_startfile = os.startfile
def hook_os_startfile(filepath, operation=None):
    if filepath.lower().endswith('.png'):
        os.system('mspaint %s' % filepath)
    else:
        org_os_startfile(filepath, operation=operation)
os.startfile = hook_os_startfile
