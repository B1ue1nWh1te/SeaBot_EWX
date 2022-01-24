import requests
import time
import json
import sys

from requests.models import Response
import Logger


try:
    Logger.info("[推送初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)
    CorpID = Setting["EnterpriseWechat"]["CorpID"]
    CorpSecret = Setting["EnterpriseWechat"]["CorpSecret"]
    AgentID = Setting["EnterpriseWechat"]["AgentID"]
    Manager = Setting["EnterpriseWechat"]["ManagerID"]
    TokenApi = Setting["EnterpriseWechat"]["TokenApi"]
    PushApi = Setting["EnterpriseWechat"]["PushApi"]
    Logger.success("[推送初始化]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Text = f'[推送初始化异常]异常信息为:{ExceptionInformation}'
    Logger.error(Text)
    sys.exit(0)


def PushToEnterpriseWechat(Type="text", Receiver="all", **kwargs):
    try:
        global CorpID, CorpSecret, AgentID, Manager, TokenApi, PushApi
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = Manager
        else:
            ToUser = Receiver
        Logger.info(f'[推送接口]正在推送至企业微信[{ToUser}]')
        Key = {"corpid": CorpID, "corpsecret": CorpSecret}
        AccessToken = {"access_token": requests.get(TokenApi, params=Key, timeout=5).json()['access_token']}
        if Type == "text":
            Time = time.strftime("%m{}%d{} %H:%M:%S").format('月', '日')
            Message = f'[{kwargs.get("Title", "无标题")}]{Time}\n{kwargs.get("Message", "")}'
            Data = {
                "touser": ToUser,
                "msgtype": "text",
                "agentid": AgentID,
                "text": {
                    "content": Message
                }
            }
        elif Type == "image_text":
            Articles = kwargs.get("Articles", [])
            if len(Articles) == 0:
                Logger.error("[推送接口]推送失败,内容为空")
                return
            Data = {
                "touser": ToUser,
                "msgtype": "news",
                "agentid": AgentID,
                "news": {"articles": Articles}
            }
        elif Type == "textcard":
            Textcard = kwargs.get("Textcard", {})
            if len(Textcard) == 0:
                Logger.error("[推送接口]推送失败,内容为空")
                return
            Textcard["btntxt"] = "查看详情"
            Data = {
                "touser": ToUser,
                "msgtype": "textcard",
                "agentid": AgentID,
                "textcard": Textcard,
            }
        else:
            Logger.error("[推送接口]推送失败,推送类型不支持")
            return
        Data = json.dumps(Data)  # 将json转换为str
        with requests.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Logger.success(f'[推送接口]推送成功,内容为:{Data}')
            else:
                Logger.error(f'[推送接口]推送失败,Response状态码为:{Response.status_code}')
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[推送接口]推送异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)


if __name__ == "__main__":
    try:
        Logger.info(f'[推送接口]主动推送模式')
        Type = input("输入消息类型:")
        if Type == "text":
            Message = input("输入指令:")
            Receiver, Title, Message = Message.split()
            flag = input("是否确定推送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat("text", Receiver, Message=Message, Title=Title)
            else:
                Logger.info(f'[推送接口]取消推送')
        elif Type == "image_text":
            Message = input("输入指令:")
            Receiver, Articles = Message.split()
            Articles = eval(Articles)
            flag = input("是否确定推送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat("image_text", Receiver, Articles=Articles)
            else:
                Logger.info(f'[推送接口]取消推送')
        elif Type == "textcard":
            Message = input("输入指令:")
            Receiver, Textcard = Message.split()
            Textcard = dict(eval(Textcard))
            flag = input("是否确定推送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat("textcard", Receiver, Textcard=Textcard)
            else:
                Logger.info(f'[推送接口]取消推送')
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[运行异常]异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        sys.exit(0)
