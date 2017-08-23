# -*- coding:utf-8 -*-

import sys
import time
import importlib
import logging


g_plugins = {}


# 添加插件目录
def addPath(pluginpath):
    if not pluginpath in sys.path:
        sys.path.insert(0, pluginpath)
        return True
    return False


# 返回当前插件列表
def modList():
    return list(g_plugins)


# 调用所有插件的此方法，参数为key=value，返回值为列表
def modCallAlls(callName, **kargs):
    retlist = []
    # logging.debug('plugin list %s' % ','.join(g_plugins))
    for mod in g_plugins:
        ret = None
        try:
            # logging.debug('call mod CallAlls %s.%s ' % (mod, callName))
            ret = modCall(mod, callName=callName, kargs=kargs)
        except Exception as e:
            import traceback
            logging.error('error call mod CallAlls：\r\n%s\r\n%s' % (str(repr(e)), traceback.format_exc()))

        retlist.append(ret)
    return retlist


# 调用某一插件的此方法，参数用 dict
def modCall(modName, callName, kargs):
    if not modName in sys.modules:
        return None

    func = getattr(sys.modules[modName], callName, None)
    if not func:
        return None

    if len(kargs) == 0:
        return func()

    return func(**kargs)


# 加载插件，如果已经有的插件，则自动卸载后重新加载
def modImport(moduleName):
    #print('modlist', sys.modules)
    if moduleName in sys.modules:
        # modRemove(sys.modules[moduleName])  # 删除后加入的变量或功能，重新加载不会被覆盖
        importlib.reload(sys.modules[moduleName])
    else:
        __import__(moduleName)

    global g_plugins
    g_plugins[moduleName] = {'loadtime': time.time()}

    return sys.modules[moduleName]


# 清除插件的所有属性等，似乎用不上
def modClearbyName(moduleNameA):
    return modClear(sys.modules[moduleNameA])


# 清除插件的所有属性等，似乎用不上
def modClear(moduleObj):
    moduledict = moduleObj.__dict__.copy()
    for ifunc in moduledict:
        if type(moduleObj.__dict__[ifunc]) == type(print):
            continue
        if ifunc.startswith('__'):
            continue
        del moduleObj.__dict__[ifunc]


# 清除掉这个插件
def modRemove(moduleName):
    global g_plugins
    print('modRemove', g_plugins)
    if moduleName in g_plugins:
        g_plugins.pop(moduleName)
    return modClearbyName(moduleName)


if __name__ == '__main__':

    import os
    botpathbase = os.path.split(os.path.split(__file__)[0])[0]
    addPath(os.path.join(botpathbase, 'plugin'))

    moduleName = 'heartbeat'
    class message(): pass
    msgobj = message()
    print(msgobj)
    msgobj.bot = 1

    b = modImport(moduleName)
    print('obj', sys.modules[moduleName])
    print('plugins', modList())
    b.test = 'hello'
    print('b.test', b.test)
    print('modCall', modCallAlls('onlogin'))
    print('modCall', modCallAlls('onmessage', msg=msgobj))
    print('modCall', modCall(moduleName, 'onmessage', kargs={'msg':msgobj}))

    modRemove(moduleName)
    print('plugins', modList())

    b = modImport(moduleName)
    print('obj', sys.modules[moduleName])
    print('b.test', getattr(b, 'test', 'no'))
    print('plugins', modList())
