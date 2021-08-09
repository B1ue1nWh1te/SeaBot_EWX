from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, jsonify, request
import xml.etree.cElementTree as ET
import requests
import json
import sys

from WXBizMsgCrypt import WXBizMsgCrypt
import Logger
import Pusher


# 初始化
try:
    Logger.Log("[主程序初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # 主程序配置
    Host = Setting["Api"]["Host"]
    Port = Setting["Api"]["Port"]
    SeaEyeApi = Setting["Main"]["SeaEyeApi"]

    # 企业微信配置
    QWX_Token = Setting["EnterpriseWechat"]["Token"]
    QWX_EncodingAESKey = Setting["EnterpriseWechat"]["EncodingAESKey"]
    QWX_CorpID = Setting["EnterpriseWechat"]["CorpID"]

    app = Flask(__name__)

    Logger.Log("[主程序初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[主程序初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 响应企业微信
@app.route('/qwx/', methods=['GET', 'POST'])
def QWX():
    # 验证
    '''msg_signature = request.args.get("msg_signature")
    timestamp=request.args.get("timestamp")
    nonce=request.args.get("nonce")
    echostr=request.args.get("echostr")
    QWX_Crypt=WXBizMsgCrypt(QWX_Token,QWX_EncodingAESKey,QWX_CorpID)
    ret,result=QWX_Crypt.VerifyURL(msg_signature, timestamp,nonce,echostr)
    print(f"{ret}\n{result}")
    return result'''
    try:
        # 接收消息
        if request.method == 'POST':
            msg_signature = request.args.get("msg_signature")
            timestamp = request.args.get("timestamp")
            nonce = request.args.get("nonce")
            data = request.data

            QWX_Crypt = WXBizMsgCrypt(QWX_Token, QWX_EncodingAESKey, QWX_CorpID)
            ret, message = QWX_Crypt.DecryptMsg(data, msg_signature, timestamp, nonce)

            XmlTree = ET.fromstring(message)
            ToUser = [XmlTree.find("FromUserName").text]
            MsgType = XmlTree.find("MsgType").text

            if MsgType == 'event':
                EventType = XmlTree.find("Event").text
                if EventType == 'click':
                    EventKey = XmlTree.find("EventKey").text
                    if EventKey == 'bilibili':
                        return Bilibili("全站", 10, "qwx", ToUser)
                    elif EventKey == 'weibo':
                        return Weibo("热搜", 10, "qwx", ToUser)
                    elif EventKey == 'zhihu':
                        return Zhihu(10, "qwx", ToUser)
                    elif EventKey == 'tonghuashun':
                        return Tonghuashun("qwx", ToUser)
                    elif EventKey == 'wangyiyun':
                        return Wangyiyun("热歌", 10, "qwx", ToUser)
                    elif EventKey == 'blog':
                        return Blog("qwx", ToUser)
                    elif EventKey == 'weather':
                        return Weather("help", "qwx", ToUser)
                    elif EventKey == 'epidemic':
                        return Epidemic("help", "qwx", ToUser)
                    elif EventKey == 'help':
                        return Help("qwx", ToUser)

            elif MsgType == 'text':
                Content = XmlTree.find("Content").text.split(" ")
                Command = Content[0]
                if len(Content) == 1:
                    if Command == "帮助":
                        return Help("qwx", ToUser)
                    elif Command == "同花顺":
                        return Tonghuashun("qwx", ToUser)
                    elif Command == "最新文章":
                        return Blog("qwx", ToUser)
                elif len(Content) == 2:
                    if Command == '天气':
                        City = Content[1]
                        return Weather(City, "qwx", ToUser)
                    elif Command == '疫情数据':
                        Province = Content[1]
                        return Epidemic(Province, "qwx", ToUser)
                    elif Command == '知乎':
                        Amount = Content[1]
                        return Zhihu(Amount, "qwx", ToUser)
                    elif Command == '网易云':
                        Type = Content[1]
                        return Wangyiyun(Type, 10, "qwx", ToUser)
                elif len(Content) == 3:
                    if Command == '哔哩哔哩':
                        Type = Content[1]
                        Amount = Content[2]
                        return Bilibili(Type, Amount, "qwx", ToUser)
                    elif Command == '微博':
                        Type = Content[1]
                        Amount = Content[2]
                        return Weibo(Type, Amount, "qwx", ToUser)

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[消息接收异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)


# 切分列表
def SplitList(List, Length):
    try:
        Temp = []
        Length = int(Length)
        for i in range(0, len(List), Length):
            Temp.append(List[i:i + Length])
        return Temp

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[切分列表异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return []


# Help事件
def Help(Platform="", ToUser=[]):
    try:
        Text = "[指令]\n(注意:[]内为变量值(不需加方括号) 词之间以空格分隔)\n\n\n<天气情况>\n天气 [地点名词]\n(如:天气 南宁)\n\n<B站排行榜>\n哔哩哔哩 [分区名] [数量](小于100)\n(如:哔哩哔哩 全站 10)\n\n<微博排行榜>\n微博 [类型] [数量](小于50)\n(如:微博 热搜 10)\n(或:微博 要闻 10)\n\n<知乎热榜>\n知乎 [数量](小于50)\n\n<同花顺快讯>\n同花顺\n\n<网易云排行榜>\n网易云 [类型]\n(类型:热歌/原创/飙升/新歌)\n(如:网易云 热歌)\n\n<疫情数据>\n疫情数据 [省份名称]\n(如:疫情数据 广西)\n\n<博客最新文章>\n最新文章\n\n<使用指南>\n帮助"

        if Platform == "":
            Logger.Log(f"[使用指南][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            Push(Receiver=ToUser, Message=Text, Title="使用指南")
            Logger.Log(f"[使用指南][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[使用指南][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[使用指南]调用函数时异常"


# Epidemic事件
def Epidemic(Province, Platform="", ToUser=[]):
    try:
        if Province == "help":
            Dict = {"data": {"Text": "查询指令:疫情数据 [省份]\n(如:疫情数据 广西  仅可省份查询)"}}
        else:
            Api = f"{SeaEyeApi}/epidemic"
            Dict = requests.get(Api, params={"province": Province}, timeout=3).json()

        if Platform == "":
            Logger.Log(f"[疫情数据][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            Push(Receiver=ToUser, Message=Dict["data"]["Text"], Title="疫情数据")
            if Province != "help":
                Push("image_text", ToUser, Articles=Dict["data"]["Articles"])
            Logger.Log(f"[疫情数据][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[疫情数据][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[疫情数据]调用函数时异常"


# Weather事件
def Weather(City, Platform="", ToUser=[]):
    try:
        if City == "help":
            Dict = {"data": "查询指令:天气 [地点名词]\n(如:天气 南宁)"}
        else:
            Api = f"{SeaEyeApi}/weather"
            Dict = requests.get(Api, params={"city": City}, timeout=3).json()

        if Platform == "":
            Logger.Log(f"[天气][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            Push(Receiver=ToUser, Message=Dict["data"], Title="天气情况")
            Logger.Log(f"[天气][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[天气][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[天气]调用函数时异常"


# Zhihu事件
def Zhihu(Amount, Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/zhihu"
        Dict = requests.get(Api, params={"amount": Amount}, timeout=3).json()
        if Dict["code"] == 200:
            Articles = SplitList(Dict["data"], 5)
            if len(Articles) == 0:
                raise Exception('SplitListError')
            #Text = f"以下是知乎热榜TOP{Amount}:"
        else:
            raise Exception('ZhihuError')

        if Platform == "":
            Logger.Log(f"[知乎][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            #Push(Message=Text, Title="知乎热榜")
            for i in Articles:
                Push("image_text", ToUser, Articles=i)
            Logger.Log(f"[知乎][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[知乎][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[知乎]调用函数时异常"


# Bilibili事件
def Bilibili(Type, Amount, Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/bilibili"
        Dict = requests.get(Api, params={"type": Type, "amount": Amount}, timeout=3).json()
        if Dict["code"] == 200:
            Articles = SplitList(Dict["data"], 5)
            if len(Articles) == 0:
                raise Exception('SplitListError')
            #Text = f"以下是[{Type}]区TOP{Amount}视频:"
        else:
            raise Exception('BilibiliError')

        if Platform == "":
            Logger.Log(f"[哔哩哔哩][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            #Push(Message=Text, Title="B站排行榜")
            for i in Articles:
                Push("image_text", ToUser, Articles=i)
            Logger.Log(f"[哔哩哔哩][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[哔哩哔哩][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[哔哩哔哩]调用函数时异常"


# Weibo事件
def Weibo(Type, Amount, Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/weibo"
        Dict = requests.get(Api, params={"type": Type, "amount": Amount}, timeout=3).json()
        if Dict["code"] == 200:
            Top = [Dict["data"][-1]]
            Dict["data"].pop(-1)
            Articles = SplitList(Dict["data"], 5)
            if len(Articles) == 0:
                raise Exception('SplitListError')
            #Text = f"以下是微博{Type}榜TOP{Amount}:"
        else:
            raise Exception('WeiboError')

        if Platform == "":
            Logger.Log(f"[微博][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            #Push(Message=Text, Title="微博排行榜")
            if not Type == "要闻":
                Push("image_text", ToUser, Articles=Top)
            for i in Articles:
                Push("image_text", ToUser, Articles=i)
            Logger.Log(f"[微博][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[微博][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[微博]调用函数时异常"


# Wangyiyun事件
def Wangyiyun(Type, Amount, Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/wangyiyun"
        Dict = requests.get(Api, params={"type": Type, "amount": Amount}, timeout=3).json()
        if Dict["code"] == 200:
            Articles = SplitList(Dict["data"], 5)
            if len(Articles) == 0:
                raise Exception('SplitListError')
            #Text = f"以下是网易云{Type}榜TOP{Amount}:"
        else:
            raise Exception('WangyiyunError')

        if Platform == "":
            Logger.Log(f"[网易云][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            #Push(Message=Text, Title="网易云排行榜")
            for i in Articles:
                Push("image_text", ToUser, Articles=i)
            Logger.Log(f"[网易云][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[网易云][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[网易云]调用函数时异常"


# Tonghuashun事件
def Tonghuashun(Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/tonghuashun"
        Dict = requests.get(Api, timeout=3).json()
        if Dict["code"] == 200:
            Tonghuashun = Dict["data"]
        else:
            raise Exception('TonghuashunError')

        if Platform == "":
            Logger.Log(f"[同花顺][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            Push("textcard", ToUser, Textcard=Tonghuashun)
            Logger.Log(f"[同花顺][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[同花顺][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[同花顺]调用函数时异常"


# Blog事件
def Blog(Platform="", ToUser=[]):
    try:
        Api = f"{SeaEyeApi}/blog"
        Dict = requests.get(Api, timeout=3).json()
        if Dict["code"] == 200:
            Articles = Dict["data"]
        else:
            raise Exception('BlogError')

        if Platform == "":
            Logger.Log(f"[博客][推送][{ToUser}]推送失败,平台未选择")
            raise Exception('PlatformError')
        elif Platform == "qwx":
            Push = Pusher.PushToEnterpriseWechat
            Push("image_text", ToUser, Articles=Articles)
            Logger.Log(f"[博客][推送][{ToUser}]推送成功")
            return ""

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[博客][运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return "[博客]调用函数时异常"


if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=5000, use_reloader=True, debug=True)
    WSGIServer((Host, Port), app).serve_forever()
