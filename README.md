<div align="center">

# SeaBot_WX

![data](https://socialify.git.ci/B1ue1nWh1te/SeaBot_WX/image?description=1&font=Rokkitt&forks=1&issues=1&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Dark)

SeaBot 计划的 微信 分支

一个能够获取新闻资讯并推送至 微信 的机器人

目前支持的信息来源有：

[微博](https://weibo.com/)、[知乎](https://www.zhihu.com/)、[哔哩哔哩](https://www.bilibili.com/)、[网易云音乐](https://music.163.com/)

[央视新闻](https://news.cctv.com/)、[同花顺快讯](https://news.10jqka.com.cn/realtimenews.html)、[百度疫情数据](https://voice.baidu.com/act/newpneumonia/newpneumonia)、[我的博客文章](https://www.seaeye.cn/)

基于 [企业微信](https://developer.work.weixin.qq.com/) 开发,通过官方插件可实现在微信同步接收消息

本项目的另一分支 [SeaBot_QQ](https://github.com/B1ue1nWh1te/SeaBot_QQ)

[![Lisence](https://img.shields.io/github/license/B1ue1nWh1te/SeaBot_WX)](https://github.com/B1ue1nWh1te/SeaBot_WX/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/B1ue1nWh1te/SeaBot_WX?include_prereleases)](https://github.com/B1ue1nWh1te/SeaBot_WX/releases/)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue)](https://www.python.org/)
[![WeCom Version](https://img.shields.io/badge/WeCom-purple)](https://developer.work.weixin.qq.com/)

</div>

# 声明

项目由 [B1ue1nWh1te](https://github.com/B1ue1nWh1te) 独立完成，若有不足的地方还请指教。

项目会保留最基本的维护(功能也许会更新吧，有时间的话- -)。

此项目仅可在合理情况下作为学习交流和个人日常使用。

# 已实现功能

- [x] [Bilibili 排行榜](https://www.bilibili.com/v/popular/all)

- [x] [微博热搜榜](https://weibo.com/ajax/statuses/hot_band)

- [x] [知乎热榜](https://www.zhihu.com/hot)

- [x] [网易云音乐排行榜](https://music.163.com/#/discover/toplist?id=3778678)

- [x] [央视新闻](https://news.cctv.com/)

- [x] [同花顺快讯](https://news.10jqka.com.cn/realtimenews.html)

- [x] [疫情数据](https://voice.baidu.com/act/newpneumonia/newpneumonia)

- [x] [博客最新文章获取(如需自定义请修改相关函数)](https://github.com/B1ue1nWh1te/SeaBot_WX/tree/main/Ability.py)

# 开始使用

## 前置准备

1. 到[企业微信](https://work.weixin.qq.com/)创建一个企业号，进入后台开启自定义机器人。
2. 参考[官方教程](https://developer.work.weixin.qq.com/document/path/90930)配置消息回调服务，代码在[Main.py](https://github.com/B1ue1nWh1te/SeaBot_WX/tree/main/Main.py)中已经写好了。
3. 参考[官方教程](https://developer.work.weixin.qq.com/document/path/90231)配置自定义菜单栏。
4. 找到以下各个参数，填入`Setting.json`的对应位置中,需要的参数有：`CorpID`、`CorpSecret`、`AgentID`、`Token`、`EncodingAESKey`、`ManagerID`。
5. (可选)如果想在微信中使用机器人而不是在企业微信中使用，那么需要在企业微信后台开启微信插件，实现消息同步接收。
6. 部署到服务器。

## 容器化部署

使用容器化部署可以让你非常快速地把机器人服务跑起来。

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

# 国内加速
# sudo curl -L "https://github.com.cnpmjs.org/docker/compose/releases/download/v2.2.2/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.2/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose

# 二进制文件应用可执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 创建命令软链接
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 查看docker-compose版本
docker-compose --version
```

假设你已经在 Linux 上安装并配置好了 docker 和 docker-compose。

```shell
# 克隆本仓库
# 国内加速 git clone https://github.com.cnpmjs.org/B1ue1nWh1te/SeaBot_WX
git clone https://github.com/B1ue1nWh1te/SeaBot_WX

# 切换至仓库目录
cd SeaBot_WX
```

修改`Setting.json`中需要自行添加的配置，其他保持默认。

配置修改完成后，在 `SeaBot_WX` 目录下打开终端，执行如下命令。

```shell
# 容器服务编排
docker-compose up -d
```

等待应用自动部署即可。

可使用如下命令查看容器的日志输出。

```shell
# 查看seabot_wx容器控制台输出
docker logs -f seabot_wx
```

一切顺利的话，很快就可以用上机器人了。

# 文档

- [企业微信 官方文档](https://developer.work.weixin.qq.com/)

# 开源许可

本项目使用 [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) 作为开源许可证。
