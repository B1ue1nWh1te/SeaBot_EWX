import requests
import time
import json
import sys

import Logger


# 初始化
try:
    Logger.Log("[推送初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # 企业微信配置
    CorpID = Setting["EnterpriseWechat"]["CorpID"]
    CorpSecret = Setting["EnterpriseWechat"]["CorpSecret"]
    AgentID = Setting["EnterpriseWechat"]["AgentID"]
    Manager = Setting["EnterpriseWechat"]["ManagerID"]
    TokenApi = Setting["EnterpriseWechat"]["TokenApi"]
    PushApi = Setting["EnterpriseWechat"]["PushApi"]

    Logger.Log("[推送初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[推送初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 推送至企业微信
def PushToEnterpriseWechat(Type="text", Receiver="all", Message="", **kwargs):
    try:
        global CorpID, CorpSecret, AgentID, Manager, TokenApi, PushApi
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = Manager
        else:
            ToUser = "|".join(Receiver)

        Logger.Log(f"[推送接口]正在推送至企业微信[{ToUser}]")
        Key = {"corpid": CorpID, "corpsecret": CorpSecret}
        AccessToken = {"access_token": requests.get(TokenApi, params=Key, timeout=3).json()['access_token']}

        if Type == "text":
            Time = time.strftime("%m{}%d{} %H:%M:%S").format('月', '日')
            Message = "[{}]{}\n{}".format(kwargs.get("Title", "未定义标题"), Time, Message)
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
                Logger.Log("[推送接口]推送失败,内容为空")
                return 0
            Data = {
                "touser": ToUser,
                "msgtype": "news",
                "agentid": AgentID,
                "news": {"articles": Articles}
            }
        elif Type == "textcard":
            Textcard = kwargs.get("Textcard", {})
            if len(Textcard) == 0:
                Logger.Log("[推送接口]推送失败,内容为空")
                return 0
            Textcard["btntxt"] = "查看详情"
            Data = {
                "touser": ToUser,
                "msgtype": "textcard",
                "agentid": AgentID,
                "textcard": Textcard,
            }

        Data = json.dumps(Data)  # 将json转换为str
        PostResponse = requests.post(PushApi, params=AccessToken, data=Data, timeout=3)

        if (PostResponse.status_code == 200):
            Logger.Log("[推送接口]推送成功,内容为:{}".format("[卡片]" if Message == "" else Message))
        else:
            Logger.Log("[推送接口]推送失败,PostResponse状态码为:{}".format(PostResponse.status_code))

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[推送接口]推送异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)


if __name__ == "__main__":
    try:
        Type = input("输入消息类型:")

        if Type == "text":
            Message = input("输入指令:")
            Receiver, Title, Message = Message.split()
            flag = input("是否确定发送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat(Type, Receiver, Message, Title=Title)
            else:
                print("取消发送")

        elif Type == "image_text":
            Message = input("输入指令:")
            Receiver, Articles = Message.split()
            Articles = eval(Articles)
            flag = input("是否确定发送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat(Type, Receiver, Articles=Articles)
            else:
                print("取消发送")

        elif Type == "textcard":
            Message = input("输入指令:")
            Receiver, Textcard = Message.split()
            Textcard = dict(eval(Textcard))
            flag = input("是否确定发送？(1/0):")
            if (flag == "1"):
                PushToEnterpriseWechat(Type, Receiver, Textcard=Textcard)
            else:
                print("取消发送")

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[运行异常]异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        sys.exit(0)
