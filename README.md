<div align="center">
    <img src="https://i.328888.xyz/2023/02/28/z23ho.png" alt="auto_teenstudy.png" border="0" width="500px" height="500px"/>
    <h1>nonebot_plugin_auto_teenstudy</h1>
    <b>基于nonebot2的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>
    <br/>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://pypi.python.org/pypi/nonebot_plugin_auto_teenstudy"><img src="https://img.shields.io/pypi/v/nonebot_plugin_auto_teenstudy?color=yellow" alt="pypi"></a>
  	<a href="https://pypi.python.org/pypi/nonebot_plugin_auto_teenstudy">
    <img src="https://img.shields.io/pypi/dm/nonebot_plugin_auto_teenstudy" alt="pypi download"></a>
		<a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://jq.qq.com/?_wv=1027&k=NGFEwXyS">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-511173803-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  </div>


## 提示
- 本插件为基础版，目前基础版可用地区Web UI版已经全部适配，请移步Web UI版
- 本插件将在暑假进行重构，请等待更新，更新期间可使用Web UI版本进行提交大学习
- Web UI 版添加用户更加方便，兼容性更高，欢迎加入QQ交流群讨论。
- 仓库地址：https://github.com/ZM25XC/TeenStudy

## 导航
* [各地区使用方式](#各地区使用方式（已经支持地区）)
* [参考](#参考)
* [安装和更新](#安装及更新)
* [导入插件](#导入插件)
* [机器人配置](#机器人配置)
* [功能列表](#功能列表)
* [提醒](#提醒)
* [说明](#说明)
* [ToDo](#ToDo)
* [更新日志](#更新日志)


## 各地区使用方式（已经支持地区）

- [江西地区](./nonebot_plugin_auto_teenstudy/resource/area/江西地区.md)
- [湖北地区](./nonebot_plugin_auto_teenstudy/resource/area/湖北地区.md)
- [浙江地区](./nonebot_plugin_auto_teenstudy/resource/area/浙江地区.md)
- [安徽地区](./nonebot_plugin_auto_teenstudy/resource/area/安徽地区.md)
- [山东地区](./nonebot_plugin_auto_teenstudy/resource/area/山东地区.md)
- [四川地区](./nonebot_plugin_auto_teenstudy/resource/area/四川地区.md)
- [上海地区](./nonebot_plugin_auto_teenstudy/resource/area/上海地区.md)
- [重庆地区](./nonebot_plugin_auto_teenstudy/resource/area/重庆地区.md)
- [吉林地区](./nonebot_plugin_auto_teenstudy/resource/area/吉林地区.md)

**其他地区努力适配中**

## 参考

- [江西共青团自动提交](https://github.com/XYZliang/JiangxiYouthStudyMaker)

- [青春湖北自动提交](https://github.com/Samueli924/TeenStudy)

- [28位openid随机生成和抓包](https://hellomango.gitee.io/mangoblog/2021/09/26/other/%E9%9D%92%E5%B9%B4%E5%A4%A7%E5%AD%A6%E4%B9%A0%E6%8A%93%E5%8C%85/)
- [定时推送大学习答案，完成截图](https://github.com/ayanamiblhx/nonebot_plugin_youthstudy)
##  安装及更新

1. 使用`git clone https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy.git`指令克隆本仓库或下载压缩包文件
2. 使用`pip install nonebot-plugin-auto-teenstudy`来进行安装,使用`pip install nonebot-plugin-auto-teenstudy -U`进行更新

## 导入插件
**使用第一种安装方式**

- 将`nonebot_plugin_auto_teenstudy`放在nb的`plugins`目录下，运行nb机器人即可

- 文件结构如下

    ```py
    📦 AweSome-Bot
    ├── 📂 awesome_bot
    │   └── 📂 plugins
    |       └── 📂 nonebot_plugin_auto_teenstudy
    |           └── 📜 __init__.py
    ├── 📜 .env
    ├── 📜 .env.dev
    ├── 📜 .env.prod
    ├── 📜 .gitignore
    ├── 📜 docker-compose.yml
    ├── 📜 Dockerfile
    ├── 📜 pyproject.toml
    └── 📜 README.md
    ```

    

**使用第二种安装方式**
- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_auto_teenstudy"]`


## 机器人配置

- 在nonebot的.env配置文件中设置好超管账号

  ```py
  SUPERUSERS=[""]
  ```
  
  


## 功能列表
|            指令            |                 指令格式                  |                             说明                             |
| :------------------------: | :---------------------------------------: | :----------------------------------------------------------: |
|         添加大学习         |     添加大学习#地区#json格式用户信息      |     各地区的json格式用户信息不同，详细查看各地区使用方式     |
|         我的大学习         |                我的大学习                 |                         查询个人信息                         |
|         提交大学习         |                提交大学习                 |                      提交最新一期大学习                      |
|           大学习           |            大学习、青年大学习             |                  获取最新一期青年大学习答案                  |
|          完成截图          |   完成截图、大学习截图、大学习完成截图    |          获取最新一期青年大学习完成截图（带状态栏）          |
|           查组织           | 查组织#地区#学校#学院名称+团委#团支部名称 |           江西、浙江地区可使用，用于查询团支部nid            |
|        个人信息截图        |        个人信息截图、青春湖北截图         |                湖北地区使用，获取个人信息截图                |
|   开启（关闭）大学习推送   |          开启（关闭）大学习推送           |                开启（关闭）大学习检查更新推送                |
| 开启（关闭）自动提交大学习 |        开启（关闭）自动提交大学习         |               开启（关闭）自动提交大学习 功能                |
|          更改信息          |          更改信息 通知方式 群聊           |        可更改项目：openid、token 、通知方式、通知群聊        |
|         大学习帮助         |     大学习帮助、大学习功能、dxx_help      |                       查看插件详细功能                       |
| 开启（关闭）大学习图片回复 |        开启（关闭）大学习图片回复         |           插件主人指令、插件回复方式，默认图片回复           |
|       设置大学习配置       | 设置大学习配置#QQ号#地区#json格式用户信息 |   插件主人指令，添加用户，json格式用户信息同添加大学习指令   |
|         删除大学习         |              删除大学习#QQ号              |                  插件主人指令，删除个人信息                  |
|     查看大学习用户列表     |            查看大学习用户列表             |                插件主人指令，查看插件用户列表                |
|       查看大学习用户       |            查看大学习用户#QQ号            |                插件主人指令，查看用户详细信息                |
|         完成大学习         |              完成大学习#QQ号              |            插件主人（团支书）指令，提交用户大学习            |
| 全局开启（关闭）大学习推送 |        全局开启（关闭）大学习推送         |         插件主人指令，用于开启（关闭）大学习更新推送         |
|    添加（删除）推送好友    |         添加（删除）推送好友#QQ号         |      插件主人指令，将用户加入（移除）大学习更新推送列表      |
|    添加（删除）推送群聊    |         添加（删除）推送群聊#群号         |      插件主人指令，将群聊加入（移除）大学习更新推送列表      |
|  查询推送群聊（好友）列表  |         查询推送群聊（好友）列表          |       插件主人指令，查看大学习更新推送群聊（好友）列表       |
|         更新大学习         |                更新大学习                 |      插件主人指令，用于手动更新青年大学习答案和完成截图      |
|         推送大学习         |                推送大学习                 |              插件主人指令，用于手动启动更新推送              |
|          一键提交          |           一键提交、全员大学习            | 插件主人（团支书）指令，一键提交所有（团支部）成员大学习，暂未解决ip池问题 |
|        执行自动提交        |               执行自动提交                |           插件主人指令，手动启动自动提交大学习功能           |
|        更改用户信息        |     更改用户信息#QQ号# 通知方式 群聊      | 插件主人指令，修改用户信息，可更改项目：openid、token 、通知方式、通知群聊 |
|          一键提醒          |                 一键提醒                  |    插件主人（团支书）指令，提醒未完成大学习成员完成大学习    |
|          一键查询          |                 一键查询                  |          插件主人（团支书）指令，查询大学习完成情况          |




## 提醒

- 本插件只适配高校，其他需要使用请前往另一仓库根据提交源码自行修改
- 不会抓包请看参考
- 需要cookie(token)的地区，抓取到cookie(token)后，请尽量别点进官方公众号，以免cookie(token)刷新
- 绝大部分地区的学校、学院和团支部名称不涉及提交，仅作为定位和标记身份。
- [各地区提交源码](https://github.com/ZM25XC/commit_dxx)

## 说明

- 一键提交、一键提醒和一键查询功能维护更新。
- 一键提醒和一键查询目前只能查询插件内的提交情况，无法查询公众号提交情况（目前已知福建、上海和安徽地区有接口可查询，正在考虑添加此功能），所以意义不大。
- ip池目前没有啥办法解决，大多地区提交大学习时验证SSL,需要https代理，目前免费的https代理少，不稳定。
- 时间精力有限，目前只维护湖北和江西两个地区，其他地区出问题请提交Issues,我找个时间修，需要增加地区可以提交Pull requests
- 觉得项目不错，不妨点个stars.

## ToDo

- [ ] 开发公众号统一推送
- [ ] 增加ip池，防止多次用同一ip导致封ip
- [ ] 增加更多地区支持
- [ ] 优化 Bot
- [ ] ~~逐步升级成群管插件~~

## 更新日志

### 2023/06/16

- 更新nonebot2强制插件元字段
- 更新依赖
- 开放吉林地区
- 移除江苏、河南、辽宁、湖南、贵州地区
- 项目进入重构阶段，请等待更新，更新期间可使用Web UI版本

### 2023/03/18

- 屏蔽湖南地区
- 屏蔽贵州地区
- 屏蔽吉林地区
- 修复重庆地区提交失败问题

### 2023/03/01

- 屏蔽辽宁地区
- 修改依赖，解决依赖冲突问题
- 更新江西地区团支部数据
- 修复江西地区提交失败问题


### 2022/09/25

- 增加湖南地区
- 增加贵州地区
- 更新江西地区团支部数据，江西地区的小伙伴请务必更新下插件
- 修复江西地区个人信息显示错误问题
- 修改图片回复图片宽度为1920px

### 2022/09/18

- 增加吉林地区
- 增加重庆地区
- 修复江西地区提交失败问题
- 调整检查更新推送间隔，减小风控
- 同步更新单地区提交源码，需要可前往另一[仓库](https://github.com/ZM25XC/commit_dxx)查看


### 2022/09/10

- 增加河南地区
- 增加江苏地区
- 增加辽宁地区
- 增加上海地区
- 增加修改用户信息功能，指令：`更改用户信息`
- 增加手动启动自动提交功能，指令：`执行自动提交`
- 分离自动提交功能，改为每周一11:30执行自动提交青年大学习功能
- 修复`更新大学习`报错问题
- 修复`设置大学习配置`指令不生效问题
- 修复安徽地区提交失败问题
- 修复湖北地区获取个人信息截图失败问题
- 修复`完成学习`指令失效问题
### 2022/09/04
- 更改添加用户方式（使用json格式添加）
- 统一用户信息存储格式
- 添加自动提交大学习功能（默认检测到大学习更新后，10~30分钟以后执行自动提交功能）
- 增加安徽地区
- 增加山东地区
- 增加四川地区
- 重新添加浙江地区
- 完成截图状态栏时间延后5~10分钟
- 支持用户修改部分信息（通知方式、通知群号、团支书QQ等）
### 2022/06/16

- 因浙江地区一个openid只能提交一个人的大学习，故移除对浙江地区支持。
- 将不支持使用机器人替多人完成大学习的地区的提交文件上传到另一[仓库](https://github.com/ZM25XC/commit_dxx)，单人使用可前往另一个[仓库](https://github.com/ZM25XC/commit_dxx)进行使用
- 添加自动检查青年大学习更新并推送功能
- 添加获取最新一期青年大学习答案和完成截图功能，完成截图功能有手机状态栏，状态栏时间会变。
- 湖北地区增加获取个人信息截图功能。
- 增加图片回复功能。
### 2022/06/05

- 增加浙江地区
- 将爬取[江西](./nonebot_plugin_auto_teenstudy/resource/crawl/crawjx.py)和[浙江](./nonebot_plugin_auto_teenstudy/resource/crawl/crawlzj.py)地区高校团支部数据（抓取nid）文件上传
### 2022/06/04

- 将代码上传至pypi，可使用`pip install nonebot-plugin-auto-teenstudy`指令安装本插件
- 增加已支持地区使用提示
- 上传基础代码
- 支持江西和湖北地区自动完成大学习（可在后台留记录）返回完成截图