import sys
import json
import requests
import Log

try:
    Log.info("[推送功能初始化]正在加载配置")
    with open("setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)["Pusher"]
    AgentID = Setting["AgentID"]
    ManagerID = Setting["ManagerID"]
    PushApi = Setting["PushApi"]
    Session = requests.session()

    Log.success("[推送功能初始化][成功]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Log.error(f'[推送功能初始化][失败]异常信息为:{ExceptionInformation}')
    sys.exit()


def PushText(Title: str, Message: str, Receiver: str = "manager") -> bool:
    from time import strftime
    try:
        global AgentID, ManagerID, PushApi
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Time = strftime("%m{}%d{} %H:%M:%S").format('月', '日')
        Message = f'[{Title}]\n[{Time}]\n\n{Message}'
        Data = {
            "touser": ToUser,
            "msgtype": "text",
            "agentid": AgentID,
            "text": {
                "content": Message
            },
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][文本消息]推送成功\n[接收者]{ToUser}\n[内容]{Message}')
                return True
            else:
                Log.error(f'[推送功能][文本消息]推送失败\n[接收者]{ToUser}\n[内容]{Message}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][文本消息]推送异常，异常信息为:{ExceptionInformation}')
        return False


def PushTextCard(Title: str, Description: str, Url: str, ButtonText: str, Receiver: str = "manager") -> bool:
    try:
        global AgentID, ManagerID, PushApi
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Textcard = {"title": Title, "description": Description, "url": Url, "btntxt": ButtonText}
        Data = {
            "touser": ToUser,
            "msgtype": "textcard",
            "agentid": AgentID,
            "textcard": Textcard,
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][文本卡片消息]推送成功\n[接收者]{ToUser}\n[内容]{Textcard}')
                return True
            else:
                Log.error(f'[推送功能][文本卡片消息]推送失败\n[接收者]{ToUser}\n[内容]{Textcard}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][文本卡片消息]推送异常，异常信息为:{ExceptionInformation}')
        return False


def PushImageTextCard(Articles: list, Receiver: str = "manager") -> bool:
    try:
        global AgentID, ManagerID, PushApi, AccessToken
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Data = {
            "touser": ToUser,
            "msgtype": "news",
            "agentid": AgentID,
            "news": {"articles": Articles},
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][图文卡片消息]推送成功\n[接收者]{ToUser}\n[内容]{Articles}')
                return True
            else:
                Log.error(f'[推送功能][图文卡片消息]推送失败\n[接收者]{ToUser}\n[内容]{Articles}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][图文卡片消息]推送异常，异常信息为:{ExceptionInformation}')
        return False


def PushButtonCard(Title: str, Description: str, Text: str, Items: list, Buttons: list, Receiver: str = "manager") -> bool:
    try:
        global AgentID, ManagerID, PushApi, AccessToken
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Data = {
            "touser": ToUser,
            "msgtype": "template_card",
            "agentid": AgentID,
            "template_card": {
                "card_type": "button_interaction",
                "main_title": {
                    "title": Title,
                    "desc": Description
                },
                "sub_title_text": Text,
                "horizontal_content_list": Items,
                "button_list": Buttons
            },
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][模板卡片消息][按钮交互型]推送成功\n[接收者]{ToUser}\n[内容]{Data["template_card"]}')
                return True
            else:
                Log.error(f'[推送功能][模板卡片消息][按钮交互型]推送失败\n[接收者]{ToUser}\n[内容]{Data["template_card"]}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][模板卡片消息][按钮交互型]推送异常，异常信息为:{ExceptionInformation}')
        return False


def PushCheckboxCard(Title: str, Description: str, QuestionKey: str, Options: list, SubmitButton: dict, Receiver: str = "manager") -> bool:
    try:
        global AgentID, ManagerID, PushApi, AccessToken
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Data = {
            "touser": ToUser,
            "msgtype": "template_card",
            "agentid": AgentID,
            "template_card": {
                "card_type": "vote_interaction",
                "main_title": {
                    "title": Title,
                    "desc": Description
                },
                "checkbox": {
                    "question_key": QuestionKey,
                    "option_list": Options,
                    "mode": 1
                },
                "submit_button": SubmitButton
            },
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][模板卡片消息][投票选择型]推送成功\n[接收者]{ToUser}\n[内容]{Data["template_card"]}')
                return True
            else:
                Log.error(f'[推送功能][模板卡片消息][投票选择型]推送失败\n[接收者]{ToUser}\n[内容]{Data["template_card"]}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][模板卡片消息][投票选择型]推送异常，异常信息为:{ExceptionInformation}')
        return False


def PushDropListCard(Title: str, Description: str, Selects: list, SubmitButton: dict, Receiver: str = "manager") -> bool:
    try:
        global AgentID, ManagerID, PushApi, AccessToken
        if Receiver == "all":
            ToUser = "@all"
        elif Receiver == "manager":
            ToUser = ManagerID
        else:
            ToUser = Receiver
        AccessToken = {"access_token": Session.get(Setting["TokenApi"], params={"corpid": Setting["CorpID"], "corpsecret": Setting["CorpSecret"]}, timeout=5).json()['access_token']}
        Data = {
            "touser": ToUser,
            "msgtype": "template_card",
            "agentid": AgentID,
            "template_card": {
                "card_type": "multiple_interaction",
                "main_title": {
                    "title": Title,
                    "desc": Description
                },
                "select_list": Selects,
                "submit_button": SubmitButton
            },
            "enable_duplicate_check": 1,
            "duplicate_check_interval": 30
        }
        Data = json.dumps(Data)
        with Session.post(PushApi, params=AccessToken, data=Data, timeout=5) as Response:
            if (Response.status_code == 200):
                Log.success(f'[推送功能][模板卡片消息][多项选择型]推送成功\n[接收者]{ToUser}\n[内容]{Data["template_card"]}')
                return True
            else:
                Log.error(f'[推送功能][模板卡片消息][多项选择型]推送失败\n[接收者]{ToUser}\n[内容]{Data["template_card"]}\n[状态码]{Response.status_code}\n[响应体]{Response.text}')
                return False
    except Exception:

        ExceptionInformation = sys.exc_info()
        Log.error(f'[推送功能][模板卡片消息][多项选择型]推送异常，异常信息为:{ExceptionInformation}')
        return False
