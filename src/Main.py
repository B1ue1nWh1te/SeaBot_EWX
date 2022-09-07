from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
import sys
import json
import Log
import Pusher
import Ability
import xml.etree.cElementTree as ET
from WXBizMsgCrypt import WXBizMsgCrypt
from flask import Flask, request


try:
    Log.info("[主程序初始化]正在加载配置")
    with open("setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)
    Host = Setting["Service"]["Host"]
    Port = Setting["Service"]["Port"]
    EWX_CorpID = Setting["Pusher"]["CorpID"]
    EWX_Token = Setting["Pusher"]["Token"]
    EWX_EncodingAESKey = Setting["Pusher"]["EncodingAESKey"]
    app = Flask(__name__)
    Log.success("[主程序初始化][成功]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Log.error(f'[主程序初始化][失败]异常信息为:{ExceptionInformation}')
    sys.exit()


def SplitList(List, Step) -> list:
    try:
        Temp = []
        for i in range(0, len(List), Step):
            Temp.append(List[i:i + Step])
        return Temp
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][切分列表][失败]异常信息为:{ExceptionInformation}')
        return None


def WeiboEvent(Receiver: str = "manager"):
    try:
        Log.info("[主程序][触发事件][微博热搜榜]开始")
        Data = SplitList(Ability.GetWeiboRank(), 5)
        for i in Data:
            Pusher.PushImageTextCard(i, Receiver)
        Log.success("[主程序][触发事件][微博热搜榜]完成")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][触发事件][微博热搜榜][失败]异常信息为:{ExceptionInformation}')
        return ""


def ZhihuEvent(Receiver: str = "manager"):
    try:
        Log.info("[主程序][触发事件][知乎热榜]开始")
        Data = SplitList(Ability.GetZhihuRank(), 5)
        for i in Data:
            Pusher.PushImageTextCard(i, Receiver)
        Log.success("[主程序][触发事件][知乎热榜]完成")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][触发事件][知乎热榜][失败]异常信息为:{ExceptionInformation}')
        return ""


def CCTVNewsEvent(Receiver: str = "manager"):
    try:
        Log.info("[主程序][触发事件][央视新闻]开始")
        Data = SplitList(Ability.GetCCTVNews(), 5)
        for i in Data:
            Pusher.PushImageTextCard(i, Receiver)
        Log.success("[主程序][触发事件][央视新闻]完成")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][触发事件][央视新闻][失败]异常信息为:{ExceptionInformation}')
        return ""


def TonghuashunEvent(Receiver: str = "manager"):
    try:
        Log.info("[主程序][触发事件][同花顺快讯]开始")
        Data = SplitList(Ability.GetTonghuashunNews(), 5)
        for i in Data:
            Pusher.PushImageTextCard(i, Receiver)
            Log.success("[主程序][触发事件][同花顺快讯]完成")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][触发事件][同花顺快讯][失败]运行异常,异常信息为:{ExceptionInformation}')
        return ""


def LeetcodeEvent(Receiver: str = "manager"):
    try:
        Log.info("[主程序][触发事件][Leetcode每日一题]开始")
        Data = Ability.GetLeetcodeEveryday()
        Pusher.PushText("Leetcode每日一题", Data, Receiver)
        Log.success("[主程序][触发事件][Leetcode每日一题]完成")
        return ""
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][触发事件][Leetcode每日一题][失败]运行异常,异常信息为:{ExceptionInformation}')
        return ""


@app.route('/seabot_ewx/', methods=['POST'])
def EWX():
    try:
        global EWX_CorpID, EWX_Token, EWX_EncodingAESKey

        '''
        # 如需进行回调服务初始化验证 请取消这段注释 然后将下面的"消息回调服务部分"注释
        # ---回调服务初始化验证部分开始---
        msg_signature = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        EWX_Crypt = WXBizMsgCrypt(EWX_Token, EWX_EncodingAESKey, EWX_CorpID)
        ret, result = EWX_Crypt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        print(f"{ret}\n{result}")
        return result
        # ---回调服务初始化验证部分结束---
        '''

        # ---消息回调服务部分开始---
        msg_signature = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        data = request.data
        EWX_Crypt = WXBizMsgCrypt(EWX_Token, EWX_EncodingAESKey, EWX_CorpID)
        ret, message = EWX_Crypt.DecryptMsg(data, msg_signature, timestamp, nonce)
        XmlTree = ET.fromstring(message)
        ToUser = XmlTree.find("FromUserName").text
        MsgType = XmlTree.find("MsgType").text
        Log.info(f'[主程序][消息回调服务][{EWX_CorpID}]接收到来自[{ToUser}]的[{MsgType}]类型消息')
        if MsgType == 'event':
            EventType = XmlTree.find("Event").text
            if EventType == 'click':
                EventKey = XmlTree.find("EventKey").text
                if EventKey == 'weibo':
                    return WeiboEvent(ToUser)
                elif EventKey == 'zhihu':
                    return ZhihuEvent(ToUser)
                elif EventKey == 'cctvnews':
                    return CCTVNewsEvent(ToUser)
                elif EventKey == 'tonghuashun':
                    return TonghuashunEvent(ToUser)
                elif EventKey == 'leetcode':
                    return LeetcodeEvent(ToUser)
        return ""
        # ---消息回调服务部分结束---
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[主程序][消息回调服务]运行异常，异常信息为:{ExceptionInformation}')
        return ""


if __name__ == '__main__':
    WSGIServer((Host, Port), app).serve_forever()
    Log.success("[主程序]服务启动成功")
