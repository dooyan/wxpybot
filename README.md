# wxpybot

[![Gitter][gitter-picture]][gitter] ![py34][py34+]

wxpybot 是基于 itchat/wxpy 开源微信个人号接口的远程机器人系统，可用于遥控树莓派树莓派raspberry

主要包括 扩展插件机制/聊天机器人/百度云盘/语音指令/远程下载/保存附件 等功能

功能尚未完成，慢慢尝试，慢慢开发

## 安装

### 下载安装代码
1 当前代码仅支持 python 3.4+ ，抱歉 python 2.x 我头痛，还是放弃支持了

### 运行前配置
1 获取百度云盘登陆认证 先在命令行执行 bypy list 按照提示获取百度授权， 此授权在同一台机子只需要获取一次
2 配置管理员账号

### 跑起来
1 执行 wxpybot
2 按照提示 扫描登陆码


## 使用

常用微信支持的指令

1 ！开头为控制指令， ## 开头是聊天机器人指令
！插件加载xxx  -- 记载plugin目录下的插件， 例如 ！插件加载demo
！插件列表     -- 当前机器人加载使用中的插件
！插件卸载xxx  -- 卸载正在使用中的某个插件， 例如 ！插件卸载demo

！心跳周期xxx  -- 心跳插件回显心跳的时间周期，默认是2小时，此心跳会发送给机器人helper账号，微信不会有新消息提示

！附件列表     -- 当前已经保存的微信附件，显示最近10个附件信息

## xxx         -- 直接和女仆机器人聊天， 例如 ##你叫什么名字


2017.8.24

