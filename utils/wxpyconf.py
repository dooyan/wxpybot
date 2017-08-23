# -*- coding:utf-8 -*-

import os

basepath = os.path.split(__file__)[0]
basepath = os.path.split(basepath)[0]

wxbot_cache_path = os.path.join(basepath, 'cache')

wxbot_loginsession_file = os.path.join(wxbot_cache_path, 'wechatlogin.token')

wxbot_loginqr_file = os.path.join(wxbot_cache_path, 'wechatloginqr.png')

wxbot_puid_file = os.path.join(wxbot_cache_path, 'wxpypuid.pkl')

