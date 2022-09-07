<div align="center">

# SeaBot_EWX

![data](https://socialify.git.ci/B1ue1nWh1te/SeaBot_EWX/image?description=1&font=Rokkitt&forks=1&issues=1&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Dark)

SeaBot_EWX 是一个能够获取新闻资讯并通过企业微信内部应用进行推送的消息机器人。

基于 [企业微信](https://developer.work.weixin.qq.com/) 开发，通过官方插件可以实现在 **微信** 同步接收消息。

[![Lisence](https://img.shields.io/github/license/B1ue1nWh1te/SeaBot_EWX)](https://github.com/B1ue1nWh1te/SeaBot_EWX/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/B1ue1nWh1te/SeaBot_EWX)](https://github.com/B1ue1nWh1te/SeaBot_EWX/releases/)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue)](https://www.python.org/)
[![EnterpriseWeChat](https://img.shields.io/badge/EnterpriseWeChat-purple)](https://developer.work.weixin.qq.com/)
[![Visitors](https://visitor-badge.glitch.me/badge?page_id=B1ue1nWh1te-SeaBot_EWX&left_color=gray&right_color=orange)](https://github.com/B1ue1nWh1te/SeaBot_EWX)

</div>

# 前言

此项目作为学习交流和个人日常使用。

# 已实现功能

- [x] [微博热搜榜](https://weibo.com/hot/search)

- [x] [知乎热榜](https://www.zhihu.com/hot)

- [x] [央视新闻](https://news.cctv.com/)

- [x] [同花顺快讯](https://news.10jqka.com.cn/realtimenews.html)

- [x] [Leetcode 每日一题](https://leetcode.cn/)

# 开始使用

## 前置准备

1. 到[企业微信](https://work.weixin.qq.com/)创建一个企业号，进入后台开启自定义机器人。
2. 参考[官方教程](https://developer.work.weixin.qq.com/document/path/90930)配置消息回调服务，代码在[Main.py](https://github.com/B1ue1nWh1te/SeaBot_EWX/tree/main/src/Main.py)中已经写好了。
3. 参考[官方教程](https://developer.work.weixin.qq.com/document/path/90231)配置自定义菜单栏，菜单栏配置文件可以参考[menu.json](https://github.com/B1ue1nWh1te/SeaBot_EWX/tree/main/menu.json)。
4. 找到以下各个参数，填入`setting.json`的对应位置中,需要的参数有：`CorpID`、`CorpSecret`、`AgentID`、`Token`、`EncodingAESKey`、`ManagerID`。
5. (可选) 如果想同时在微信中使用机器人，那么需要在企业微信后台开启微信插件，实现消息同步接收。
6. 部署到服务器。

## 容器化部署

CentOS 下安装 docker 和 docker-compose:

```shell
# 一键安装docker
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun

# 查看docker版本
docker -v

# 设置开机启动
systemctl enable docker

# 启动
systemctl start docker



# 安装docker-compose
pip3 install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose

# 二进制文件应用可执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 创建命令软链接
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 查看docker-compose版本
docker-compose --version
```

在 Linux 上安装好 docker 和 docker-compose 之后：

```shell
# 克隆本仓库
git clone https://github.com/B1ue1nWh1te/SeaBot_EWX

# 切换至仓库目录
cd SeaBot_EWX
```

修改`setting.json`中需要自行添加的配置，其他保持默认。

配置修改完成后，在 `SeaBot_EWX` 目录下打开终端，执行如下命令。

```shell
# 容器服务编排
docker-compose up -d
```

等待应用自动部署即可。

可使用如下命令查看容器的日志输出。

```shell
# 查看seabot_ewx容器控制台输出
docker logs -f seabot_ewx
```

# 文档

- [企业微信 官方文档](https://developer.work.weixin.qq.com/)

# 开源许可

本项目使用 [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) 作为开源许可证。
