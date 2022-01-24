from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, request
import xml.etree.cElementTree as ET
import json
import sys
from WXBizMsgCrypt import WXBizMsgCrypt
import Logger
import Ability
import Pusher


try:
    Logger.info("[主程序初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)
    Host = Setting["Service"]["Host"]
    Port = Setting["Service"]["Port"]
    QWX_Token = Setting["EnterpriseWechat"]["Token"]
    QWX_EncodingAESKey = Setting["EnterpriseWechat"]["EncodingAESKey"]
    QWX_CorpID = Setting["EnterpriseWechat"]["CorpID"]
    Push = Pusher.PushToEnterpriseWechat
    app = Flask(__name__)
    Logger.success("[主程序初始化]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Text = f'[主程序初始化异常]异常信息为:{ExceptionInformation}'
    Logger.error(Text)
    sys.exit(0)


# 响应企业微信
@app.route('/qwx/', methods=['POST'])
def QWX():
    try:
        '''回调服务初始化验证 如需使用请取消这段注释 然后将下面的"接收消息"段注释掉
        msg_signature = request.args.get("msg_signature")
        timestamp=request.args.get("timestamp")
        nonce=request.args.get("nonce")
        echostr=request.args.get("echostr")
        QWX_Crypt=WXBizMsgCrypt(QWX_Token,QWX_EncodingAESKey,QWX_CorpID)
        ret,result=QWX_Crypt.VerifyURL(msg_signature, timestamp,nonce,echostr)
        print(f"{ret}\n{result}")
        return result'''

        # ---接收消息---
        msg_signature = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        data = request.data
        QWX_Crypt = WXBizMsgCrypt(QWX_Token, QWX_EncodingAESKey, QWX_CorpID)
        ret, message = QWX_Crypt.DecryptMsg(data, msg_signature, timestamp, nonce)
        XmlTree = ET.fromstring(message)
        ToUser = XmlTree.find("FromUserName").text
        MsgType = XmlTree.find("MsgType").text
        Logger.info(f'[消息接收接口]接收到来自[{ToUser}]的[{MsgType}]类型消息')
        if MsgType == 'event':
            EventType = XmlTree.find("Event").text
            if EventType == 'click':
                EventKey = XmlTree.find("EventKey").text
                if EventKey == 'bilibili':
                    return Bilibili(ToUser=ToUser)
                elif EventKey == 'weibo':
                    return Weibo(ToUser=ToUser)
                elif EventKey == 'zhihu':
                    return Zhihu(ToUser=ToUser)
                elif EventKey == 'cctvnews':
                    return CCTVNews(ToUser=ToUser)
                elif EventKey == 'tonghuashun':
                    return Tonghuashun(ToUser=ToUser)
                elif EventKey == 'wangyiyun':
                    return Wangyiyun(ToUser=ToUser)
                elif EventKey == 'blog':
                    return Blog(ToUser=ToUser)
                elif EventKey == 'epidemic':
                    return Epidemic(ToUser=ToUser)
                elif EventKey == 'help':
                    return Help(ToUser=ToUser)
        elif MsgType == 'text':
            Content = XmlTree.find("Content").text.split(" ")
            Command = Content[0]
            if len(Content) == 1:
                if Command == '帮助':
                    return Help(ToUser=ToUser)
                elif Command == '同花顺快讯':
                    return Tonghuashun(ToUser=ToUser)
                elif Command == '最新文章':
                    return Blog(ToUser=ToUser)
            elif len(Content) == 2:
                if Command == '疫情数据':
                    Province = Content[1]
                    return Epidemic(Province, ToUser)
                elif Command == '知乎':
                    Amount = Content[1]
                    return Zhihu(Amount, ToUser)
                elif Command == '微博':
                    Amount = Content[1]
                    return Weibo(Amount, ToUser)
                elif Command == '央视新闻':
                    Amount = Content[1]
                    return CCTVNews(Amount, ToUser)
            elif len(Content) == 3:
                if Command == '哔哩哔哩':
                    Type = Content[1]
                    Amount = Content[2]
                    return Bilibili(Type, Amount, ToUser)
                elif Command == '网易云音乐':
                    Type = Content[1]
                    Amount = Content[2]
                    return Wangyiyun(Type, Amount, ToUser)
        # ---接收消息---
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[消息接收接口]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# 切分列表
def SplitList(List, Length):
    try:
        Temp = []
        Length = Length
        for i in range(0, len(List), Length):
            Temp.append(List[i:i + Length])
        return Temp
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[切分列表异常]异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


# Help事件
def Help(ToUser):
    try:
        Logger.info("[事件触发-使用指南]")
        Text = "\n<B站排行榜>\n哔哩哔哩 分区名 数量\n(如:哔哩哔哩 全站 10)\n\n<微博热搜榜>\n微博 数量\n(如:微博 10)\n\n<知乎热榜>\n知乎 数量\n\n<央视新闻>\n央视新闻 数量\n\n<同花顺快讯>\n同花顺快讯\n\n<网易云音乐排行榜>\n网易云音乐 分区 数量\n(类型:热歌/原创/飙升/新歌)\n(如:网易云 热歌 10)\n\n<疫情数据>\n疫情数据 省份名称\n(如:疫情数据 广西)\n\n<博客最新文章>\n最新文章\n\n<使用指南>\n帮助"
        Push(Receiver=ToUser, Message=Text, Title="使用指南")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[使用指南]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Epidemic事件
def Epidemic(Province="help", ToUser=""):
    try:
        Logger.info("[事件触发-疫情数据]")
        if Province == "help":
            Text = "查询指令:疫情数据 省份名称\n(如:疫情数据 广西)"
            Push(Receiver=ToUser, Message=Text, Title="疫情数据")
        else:
            Data = Ability.GetEpidemicData(Province)
            Text = Data["Text"]
            Articles = Data["Articles"]
            Push(Receiver=ToUser, Message=Text, Title="疫情数据")
            Push("image_text", ToUser, Articles=Articles)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[疫情数据]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Zhihu事件
def Zhihu(Amount=10, ToUser=""):
    try:
        Logger.info("[事件触发-知乎热榜]")
        Data = Ability.GetZhihuRank(Amount)
        Articles = SplitList(Data, 5)
        for i in Articles:
            Push("image_text", ToUser, Articles=i)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[知乎热榜]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Bilibili事件
def Bilibili(Type="全站", Amount=10, ToUser=""):
    try:
        Logger.info("[事件触发-B站排行榜]")
        Data = Ability.GetBilibiliRank(Type, Amount)
        Articles = SplitList(Data, 5)
        for i in Articles:
            Push("image_text", ToUser, Articles=i)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[B站排行榜]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Weibo事件
def Weibo(Amount=10, ToUser=""):
    try:
        Logger.info("[事件触发-微博热搜榜]")
        Data = Ability.GetWeiboRank(Amount)
        Top = [Data[-1]]
        Push("image_text", ToUser, Articles=Top)
        Data.pop(-1)
        Articles = SplitList(Data, 5)
        for i in Articles:
            Push("image_text", ToUser, Articles=i)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[微博热搜榜]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Wangyiyun事件
def Wangyiyun(Type="热歌", Amount=10, ToUser=""):
    try:
        Logger.info("[事件触发-网易云音乐排行榜]")
        Data = Ability.GetWangyiyunRank(Type, Amount)
        Articles = SplitList(Data, 5)
        for i in Articles:
            Push("image_text", ToUser, Articles=i)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[网易云音乐排行榜]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Tonghuashun事件
def Tonghuashun(ToUser):
    try:
        Logger.info("[事件触发-同花顺快讯]")
        Data = Ability.GetTonghuashunNews()
        Push("textcard", ToUser, Textcard=Data)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[同花顺快讯]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# Blog事件
def Blog(ToUser):
    try:
        Logger.info("[事件触发-博客文章]")
        Data = Ability.GetBlog()
        Push("image_text", ToUser, Articles=Data)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[博客文章]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


# CCTVNews事件
def CCTVNews(Amount=10, ToUser=""):
    try:
        Logger.info("[事件触发-央视新闻]")
        Data = Ability.GetCCTVNews(Amount)
        Articles = SplitList(Data, 5)
        for i in Articles:
            Push("image_text", ToUser, Articles=i)
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[央视新闻]运行异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return ""


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000, use_reloader=True, debug=True)
    Logger.info("[服务启动]启动服务")
    WSGIServer((Host, Port), app).serve_forever()
