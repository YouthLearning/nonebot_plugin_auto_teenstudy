<div align="center">
    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>
    <h1>nonebot_plugin_auto_teenstudy</h1>
    <b>基于nonebot2的青年大学习自动提交插件，用于自动完成大学习，在后台留下记录，返回完成截图</b>
    <br/>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
    <a href="https://github.com/ZM25XC/nonebot_plugin_auto_teenstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ZM25XC/nonebot_plugin_auto_teenstudy?style=flat-square"></a>
</div>


## 各地区使用方式（已经支持地区）

- [江西地区](./nonebot_plugin_auto_teenstudy/resource/江西地区.md)
- [湖北地区](./nonebot_plugin_auto_teenstudy/resource/湖北地区.md)

## 已抓包分析但机器人不支持使用的地区请前往另一个仓库
- [点我去另一个仓库](https://github.com/ZM25XC/commit_dxx)

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

**使用第二种安装方式**
- 在`bot.py`中添加`nonebot.load_plugin("nonebot_plugin_auto_teenstudy")`或在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_auto_teenstudy"]`


## 机器人配置

- 在nonebot的.env配置文件中设置好超管账号

  ```py
  SUPERUSERS=[""]
  ```


- 请确保已安装以下第三方库（插件运行失败请检查第三方库有没有装完整）

  ```py
  asyncio 
  anti_useragent 
  secrets
  httpx
  string
  bs4
  PIL
  ```

  

## 功能列表

### 大学习

```py
一、主人专用
1、添加大学习配置|添加大学习用户|add_dxx
指令格式：添加大学习配置#QQ号#地区#姓名#学校#团委(学院)#团支部(班级)
2、删除大学习配置|删除大学习用户|del_dxx
指令格式：删除大学习配置#QQ号
3、查看大学习用户列表
4、查看大学习用户|查看大学习配置|check_dxx_user
指令格式：查看大学习用户#QQ号
5、完成大学习|finish_dxx
指令格式：完成大学习#QQ号
6、添加（删除）推送好友
指令格式：添加推送好友#QQ号
7、添加（删除）推送群聊
指令格式：添加（删除）推送群聊#群号
8、查询推送好友（群聊）列表
9、全局开启（关闭）大学习推送
10、大学习图片回复开（关）|开启（关闭）大学习图片回复
二、全员可用
1、提交大学习
2、我的大学习|查看我的大学习|my_dxx
3、大学习功能|大学习帮助|dxx_help
4、大学习|青年大学习
5、大学习完成截图|完成截图|dxx_end
6、设置大学习配置|set_dxx
指令格式：设置大学习配置#地区#姓名#学校#团委(学院)#团支部(班级)
7、个人信息截图|青春湖北截图（此功能只支持湖北用户）
8、查组织|查班级|check_class
指令格式：查组织#地区简写(例江西为：jx)#学校名称#团委名称
Ps:查组织功能对湖北用户无效！
```

## To Do
- [ ] 增加ip池，防止多次用同一ip导致封ip
- [ ] 增加更多地区支持
- [ ] 优化 Bot
- [ ] ~~逐步升级成群管插件~~

## 更新日志

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