import requests
import time
import json
import sys
import re

import Logger


# 初始化
try:
    Logger.Log("[使能初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # 使能配置
    Headers = Setting["Ability"]["Headers"]

    WeatherApi = Setting["Ability"]["WeatherApi"]

    BilibiliRankApi = Setting["Ability"]["BilibiliRankApi"]
    BilibiliImageApi = Setting["Ability"]["BilibiliImageApi"]
    BilibiliTypeMap = Setting["Ability"]["BilibiliTypeMap"]

    WeiboRankApi = Setting["Ability"]["WeiboRankApi"]
    WeiboTopImage = Setting["Ability"]["WeiboTopImage"]
    WeiboTopTypeMap = Setting["Ability"]["WeiboTopTypeMap"]

    ZhihuRankApi = Setting["Ability"]["ZhihuRankApi"]
    ZhihuQuestionApi = Setting["Ability"]["ZhihuQuestionApi"]

    TonghuashunApi = Setting["Ability"]["TonghuashunApi"]

    WangyiyunRankApi = Setting["Ability"]["WangyiyunRankApi"]
    WangyiyunSongApi = Setting["Ability"]["WangyiyunSongApi"]
    WangyiyunTypeMap = Setting["Ability"]["WangyiyunTypeMap"]

    BaiduEpidemicDataApi = Setting["Ability"]["BaiduEpidemicDataApi"]
    BaiduEpidemicNewsApi = Setting["Ability"]["BaiduEpidemicNewsApi"]

    BlogApi = Setting["Ability"]["BlogApi"]

    Logger.Log("[使能初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[使能初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 获取天气
def GetWeather(City=""):
    try:
        if City == "":
            Logger.Log(f"[天气接口]未输入城市名称,获取[{City}]天气失败")
            return {"code": 404, "data": "获取天气失败\n请输入城市名称", "msg": "失败"}
        Logger.Log(f"[天气接口]正在获取[{City}]天气")
        WeatherDict = requests.get(WeatherApi, params={"city": City}, headers=Headers, timeout=3).json()

        if WeatherDict["status"] != 1000:
            Logger.Log(f"[天气接口]输入的城市名称不正确,获取[{City}]天气失败")
            return {"code": 404, "data": "获取天气失败\n请检查输入的城市名称是否正确", "msg": "失败"}

        WeatherDict = WeatherDict["data"]["forecast"]
        WeatherDetail = "[地点-{}]\n今日天气:{} {}/{}\n明日天气:{} {}/{}".format(City, WeatherDict[0]["type"], WeatherDict[0]["high"].replace("高温 ", ""), WeatherDict[0]
                                                                       ["low"].replace("低温 ", ""), WeatherDict[1]["type"], WeatherDict[1]["high"].replace("高温 ", ""), WeatherDict[1]["low"].replace("低温 ", ""))
        Logger.Log(f"[天气接口]获取[{City}]天气成功")
        return {"code": 200, "city": City, "data": WeatherDetail, "msg": "成功"}

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[天气接口]获取天气异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        return {"code": 404, "data": "获取天气失败\n程序运行错误或数据接口异常", "msg": "失败"}


# 获取Bilibili排行榜
def GetBilibiliRank(Type="全站", Amount=10):
    try:
        if Type not in BilibiliTypeMap:
            Type = "全站"
        Logger.Log(f"[Bilibili接口]正在获取[{Type}]排行榜信息")
        Data = {"code": 200, "class": Type, "data": [], "msg": "成功"}

        Api = f"{BilibiliRankApi}{BilibiliTypeMap[Type]}"
        RawText = requests.get(Api, headers=Headers, timeout=3).text.replace(" ", "").replace("\n", "")
        Titles = re.findall('<ahref=".*?"target="_blank"class="title">(.*?)</a>', RawText)
        Urls = re.findall('<divclass="img"><ahref="(.*?)"target="_blank">', RawText)
        Authors = re.findall('<iclass="b-iconauthor"></i>(.*?)</span>', RawText)
        t = "---".join(Urls)
        BVs = re.findall('//www.bilibili.com/video/(.*?)---', t)

        for i in range(Amount):
            ImageUrl = requests.get(BilibiliImageApi, params={"bvid": BVs[i]}, headers=Headers, timeout=3).json()["data"]["pic"]
            Temp = {
                'title': f"[No.{i+1}]{Titles[i]}[{Authors[i]}]",
                'url': f'https:{Urls[i]}',
                'picurl': ImageUrl
            }
            Data["data"].append(Temp)

        Logger.Log(f"[Bilibili接口]获取[{Type}]排行榜信息成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[Bilibili接口]获取B站排行榜异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data


# 获取微博排行榜
def GetWeiboRank(Type="热搜", Amount=10):
    try:
        if Type not in WeiboTopTypeMap:
            Type = "热搜"
        Logger.Log(f"[微博接口]正在获取[{Type}]榜信息")
        Data = {"code": 200, "class": Type, "data": [], "msg": "成功"}

        RawText = requests.get(WeiboRankApi, params={"cate": WeiboTopTypeMap[Type]}, headers=Headers, timeout=3).text.replace(" ", "").replace("\n", "")
        if Type == "要闻":
            Urls = re.findall('<tdclass="td-01ranktop"><iclass="icon-dot"></i></td><tdclass="td-02"><ahref="(.*?)"target="_blank">.*?</a>', RawText)
            Titles = re.findall('<tdclass="td-01ranktop"><iclass="icon-dot"></i></td><tdclass="td-02"><ahref=".*?"target="_blank">(.*?)</a>', RawText)
            TopUrl = TopTitle = []
        else:
            Urls = re.findall('<tdclass="td-01ranktop">\d+</td><tdclass="td-02"><ahref="(.*?)"target="_blank">.*?</a>', RawText)
            Titles = re.findall('<tdclass="td-01ranktop">\d+</td><tdclass="td-02"><ahref=".*?"target="_blank">(.*?)</a>', RawText)
            TopUrl = re.findall('<tdclass="td-01"><iclass="icon-top"></i></td><tdclass="td-02"><ahref="(.*?)"target="_blank">.*?</a></td>', RawText)
            TopTitle = re.findall('<tdclass="td-01"><iclass="icon-top"></i></td><tdclass="td-02"><ahref=".*?"target="_blank">(.*?)</a></td>', RawText)

        for i in range(Amount):
            Temp = {
                'title': f"[No.{i+1}]{Titles[i]}",
                'url': f'https://s.weibo.com{Urls[i]}',
                'picurl': ''
            }
            Data["data"].append(Temp)
        if len(TopUrl) != 0 and len(TopTitle) != 0:
            Data["data"].append({'title': f"[置顶]{TopTitle[0]}", 'url': f'https://s.weibo.com{TopUrl[0]}', 'picurl': WeiboTopImage})

        Logger.Log(f"[微博接口]获取[{Type}]榜信息成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[微博接口]获取微博排行榜异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data


# 获取知乎热榜
def GetZhihuRank(Amount=10):
    try:
        Logger.Log("[知乎接口]正在获取知乎热榜信息")
        Dict = requests.get(ZhihuRankApi, headers=Headers, timeout=3).json()["data"]
        Data = {"code": 200, "data": [], "msg": "成功"}

        for i in range(Amount):
            Temp = {
                'title': f'[No.{i+1}]{Dict[i]["target"]["title"]}',
                'url': f'{ZhihuQuestionApi}{Dict[i]["target"]["id"]}',
                'picurl': Dict[i]["children"][0]["thumbnail"]
            }
            Data["data"].append(Temp)

        Logger.Log("[知乎接口]获取知乎热榜信息成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[知乎接口]获取知乎热榜异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data


# 获取同花顺快讯
def GetTonghuashunNews():
    try:
        Logger.Log("[同花顺接口]正在获取同花顺快讯")
        Dict = requests.get(TonghuashunApi, headers=Headers, timeout=3).json()["data"]["list"][0]
        Data = {
            "code": 200,
            "data": {
                'id': Dict["id"],
                'title': f'[同花顺快讯]{Dict["title"]}',
                'description': Dict["digest"],
                'url': Dict["appUrl"]
            },
            "msg": "成功"
        }

        Logger.Log("[同花顺接口]获取同花顺快讯成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[同花顺接口]获取同花顺快讯异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data


# 获取网易云音乐排行榜
def GetWangyiyunRank(Type="热歌", Amount=10):
    try:
        if Type not in WangyiyunTypeMap:
            Type = "热歌"
        Logger.Log(f"[网易云接口]正在获取网易云音乐{Type}榜")
        Data = {"code": 200, "class": Type, "data": [], "msg": "成功"}

        Dict = requests.get(WangyiyunRankApi, params={"id": WangyiyunTypeMap[Type]}, headers=Headers, timeout=3).json()["playlist"]["tracks"]
        for i in range(Amount):
            Singers = []
            for j in Dict[i]["ar"]:
                Singers.append(j["name"])
            Singers = "/".join(Singers)
            Temp = {
                'title': f'[No.{i+1}]   {Dict[i]["name"]}   [{Singers}]',
                'url': f'{WangyiyunSongApi}?id={Dict[i]["id"]}',
                'picurl': f'{Dict[i]["al"]["picUrl"]}?param=200y200&quality=100'
            }
            Data["data"].append(Temp)

        Logger.Log(f"[网易云接口]获取网易云音乐{Type}榜成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[网易云接口]获取网易云音乐排行榜异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data


# 获取国内疫情数据
def GetEpidemicData(Province=""):
    try:
        if Province == "":
            Logger.Log(f"[疫情数据接口]未输入省份名称,获取疫情数据失败")
            return {"code": 404, "data": "获取疫情数据失败\n请输入省份名称", "msg": "失败"}

        Logger.Log(f"[疫情数据接口]正在获取[{Province}]疫情数据")
        Params = {"target": "trend", "isCaseIn": 1, "from": "mola-virus", "area": Province, "stage": "publish"}
        Dict = requests.get(BaiduEpidemicDataApi, params=Params, headers=Headers, timeout=3).json()["data"][0]["trend"]
        Date = Dict["updateDate"][-1].replace(".", "月") + "日"
        NewDiagnose = Dict["list"][3]["data"][-1]
        NowDiagnose = Dict["list"][0]["data"][-1] - (Dict["list"][1]["data"][-1] + Dict["list"][2]["data"][-1])
        Text = f"[{Date}]{Province}疫情数据:\n新增确诊:{NewDiagnose}\n现有确诊:{NowDiagnose}\n\n[数据来源:百度数据]"

        Params = {"tn": "reserved_all_res_tn", "dspName": "iphone", "from_sf": 1, "dsp": "iphone", "resource_id": 28565, "alr": 1, "query": f"{Province}新型肺炎最新动态"}
        List = requests.get(BaiduEpidemicNewsApi, params=Params, headers=Headers, timeout=3).json()["Result"][0]["items_v2"][0]["aladdin_res"]["DisplayData"]["result"]["items"]
        Articles = []
        for i in range(5):
            timetemp = time.localtime(int(List[i]["eventTime"]))
            Date = time.strftime("%m{}%d{} %H:%M", timetemp).format('月', '日')
            Temp = {
                'title': f'[{Date}]{List[i]["eventDescription"]}',
                'url': List[i]["eventUrl"].replace("\\", ""),
            }
            Articles.append(Temp)
        Data = {'code': 200, 'data': {'Text': Text, 'Articles': Articles}, 'msg': '成功'}

        Logger.Log(f"[疫情数据接口]获取[{Province}]疫情数据成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[疫情数据接口]获取疫情数据异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "data": "获取疫情数据失败\n程序运行错误或接口异常", "msg": "失败"}
        return Data


# 获取博客最新文章
def GetBlog():
    try:
        Logger.Log(f"[博客接口]正在获取最新博客文章")
        RawText = requests.get(BlogApi, headers=Headers, timeout=3).text.replace(" ", "").replace("\n", "")
        Urls = re.findall('<h1><aclass="text-default"href="(.*?)">.*?</a></h1>', RawText)
        Titles = re.findall('<h1><aclass="text-default"href=".*?">(.*?)</a></h1>', RawText)
        Data = {'code': 200, 'data': [], 'msg': '成功'}

        for i in range(len(Urls)):
            Temp = {
                'title': f"[No.{i+1}]{Titles[i]}",
                'url': Urls[i],
            }
            Data["data"].append(Temp)

        Logger.Log(f"[博客接口]获取最新博客文章成功")
        return Data

    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = "[博客接口]获取最新博客文章异常,异常信息为:{}".format(ExceptionInformation)
        Logger.Log(Text)
        Data = {"code": 404, "msg": "失败"}
        return Data
