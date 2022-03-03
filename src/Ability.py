from http.client import responses
import requests
import time
import json
import sys
import re
import Logger


try:
    Logger.info("[功能初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)
    Headers = Setting["Ability"]["Headers"]
    BilibiliRankApi = Setting["Ability"]["BilibiliRankApi"]
    BilibiliImageApi = Setting["Ability"]["BilibiliImageApi"]
    BilibiliTypeMap = Setting["Ability"]["BilibiliTypeMap"]
    WeiboRankApi = Setting["Ability"]["WeiboRankApi"]
    WeiboTopImageUrl = Setting["Ability"]["WeiboTopImageUrl"]
    ZhihuRankApi = Setting["Ability"]["ZhihuRankApi"]
    ZhihuQuestionApi = Setting["Ability"]["ZhihuQuestionApi"]
    TonghuashunApi = Setting["Ability"]["TonghuashunApi"]
    CCTVNewsApi = Setting["Ability"]["CCTVNewsApi"]
    WangyiyunRankApi = Setting["Ability"]["WangyiyunRankApi"]
    WangyiyunSongApi = Setting["Ability"]["WangyiyunSongApi"]
    WangyiyunTypeMap = Setting["Ability"]["WangyiyunTypeMap"]
    BaiduEpidemicDataApi = Setting["Ability"]["BaiduEpidemicDataApi"]
    BaiduEpidemicNewsApi = Setting["Ability"]["BaiduEpidemicNewsApi"]
    BlogApi = Setting["Ability"]["BlogApi"]
    Logger.success("[功能初始化]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Text = f'[功能初始化异常]异常信息为:{ExceptionInformation}'
    Logger.error(Text)
    sys.exit(0)


def GetBilibiliRank(Type="全站", Amount=10):
    try:
        TypeId = BilibiliTypeMap.get(Type, BilibiliTypeMap["全站"])
        Logger.info(f'[哔哩哔哩接口]正在获取[{Type}]排行榜信息')
        Data = []
        Url = f'{BilibiliRankApi}{TypeId}'
        RawText = requests.get(Url, headers=Headers, timeout=5).text.replace(" ", "").replace("\n", "")
        Titles = re.findall('<ahref=".*?"target="_blank"class="title">(.*?)</a>', RawText)
        VideoUrls = re.findall('<divclass="img"><ahref="(.*?)"target="_blank">', RawText)
        Authors = re.findall('<spanclass="data-boxup-name"><imgsrc=".*?"alt="up">(.*?)</span>', RawText)
        Temp = "---".join(VideoUrls)
        BVs = re.findall('//www.bilibili.com/video/(.*?)---', Temp)
        for i in range(Amount):
            ImageUrl = requests.get(BilibiliImageApi, params={"bvid": BVs[i]}, headers=Headers, timeout=5).json()["data"]["pic"]
            Temp = {
                'title': f'[No.{i+1}] {Titles[i]} [{Authors[i]}]',
                'url': f'https:{VideoUrls[i]}',
                'picurl': ImageUrl
            }
            Data.append(Temp)
        Logger.success(f'[哔哩哔哩接口]获取[{Type}]排行榜信息成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[哔哩哔哩接口]获取[{Type}]排行榜信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetWeiboRank(Amount=10):
    try:
        Logger.info("[微博接口]正在获取热搜榜信息")
        Data = []
        RawData = requests.get(WeiboRankApi, headers=Headers, timeout=5).json()
        TopTitle = f'[置顶]{RawData["data"]["hotgov"]["name"]}'
        TopUrl = f'https://s.weibo.com/weibo?q={RawData["data"]["hotgov"]["name"]}'
        Result = RawData["data"]["band_list"]
        for i in range(Amount):
            Temp = {
                'title': f'[No.{i+1}]{Result[i]["note"]}',
                'url': f'https://s.weibo.com/weibo?q=%23{Result[i]["note"]}%23',
                'picurl': ''
            }
            Data.append(Temp)
        Data.append({'title': TopTitle, 'url': TopUrl, 'picurl': WeiboTopImageUrl})
        Logger.success(f'[微博接口]获取热搜榜信息成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[微博接口]获取排行榜信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetZhihuRank(Amount=10):
    try:
        Logger.info("[知乎接口]正在获取热榜信息")
        RawData = requests.get(ZhihuRankApi, headers=Headers, timeout=5).json()["data"]
        Data = []
        for i in range(Amount):
            Temp = {
                'title': f'[No.{i+1}]{RawData[i]["target"]["title"]}',
                'url': f'{ZhihuQuestionApi}{RawData[i]["target"]["id"]}',
                'picurl': RawData[i]["children"][0]["thumbnail"]
            }
            Data.append(Temp)
        Logger.success("[知乎接口]获取热榜信息成功")
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[知乎接口]获取热榜信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetTonghuashunNews():
    try:
        Logger.info("[同花顺接口]正在获取快讯信息")
        RawData = requests.get(TonghuashunApi, headers=Headers, timeout=5).json()["data"]["list"][0]
        Data = {
            'id': RawData["id"],
            'title': f'[同花顺快讯]{RawData["title"]}',
            'description': RawData["digest"],
            'url': RawData["appUrl"]
        }
        Logger.success("[同花顺接口]获取快讯信息成功")
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[同花顺接口]获取快讯信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetWangyiyunRank(Type="热歌", Amount=10):
    try:
        TypeId = WangyiyunTypeMap.get(Type, WangyiyunTypeMap["热歌"])
        Logger.info(f'[网易云音乐接口]正在获取{Type}排行榜信息')
        Data = []
        RawData = requests.get(WangyiyunRankApi, params={"id": TypeId}, headers=Headers, timeout=5).json()["playlist"]["tracks"]
        for i in range(Amount):
            Singers = []
            for j in RawData[i]["ar"]:
                Singers.append(j["name"])
            Singers = "/".join(Singers)
            Temp = {
                'title': f'[No.{i+1}] {RawData[i]["name"]} [{Singers}]',
                'url': f'{WangyiyunSongApi}?id={RawData[i]["id"]}',
                'picurl': f'{RawData[i]["al"]["picUrl"]}?param=200y200&quality=100'
            }
            Data.append(Temp)
        Logger.success(f'[网易云音乐接口]获取{Type}排行榜信息成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[网易云音乐接口]获取{Type}排行榜信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetEpidemicData(Province):
    try:
        Logger.info(f'[疫情数据接口]正在获取[{Province}]疫情数据')
        Params = {"target": "trend", "isCaseIn": 1, "from": "mola-virus", "area": Province, "stage": "publish"}
        RawData = requests.get(BaiduEpidemicDataApi, params=Params, headers=Headers, timeout=5).json()["data"][0]["trend"]
        Date = f'{RawData["updateDate"][-1].replace(".", "月")}日'
        NewDiagnose = RawData["list"][3]["data"][-1]
        NowDiagnose = RawData["list"][0]["data"][-1] - (RawData["list"][1]["data"][-1] + RawData["list"][2]["data"][-1])
        Text = f'[{Date}]{Province}疫情数据:\n新增确诊:{NewDiagnose}\n现有确诊:{NowDiagnose}\n[来源:百度数据]'
        Params = {"tn": "reserved_all_res_tn", "dspName": "iphone", "from_sf": 1, "dsp": "iphone", "resource_id": 28565, "alr": 1, "query": f"{Province}新型肺炎最新动态"}
        List = requests.get(BaiduEpidemicNewsApi, params=Params, headers=Headers, timeout=5).json()["Result"][0]["items_v2"][0]["aladdin_res"]["DisplayData"]["result"]["items"]
        Articles = []
        for i in range(5):
            TimeTemp = time.localtime(int(List[i]["eventTime"]))
            Date = time.strftime("%m{}%d{} %H:%M", TimeTemp).format('月', '日')
            Temp = {
                'title': f'[{Date}]{List[i]["eventDescription"]}',
                'url': List[i]["eventUrl"].replace("\\", ""),
            }
            Articles.append(Temp)
        Data = {'Text': Text, 'Articles': Articles}
        Logger.success(f'[疫情数据接口]获取[{Province}]疫情数据成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[疫情数据接口]获取[{Province}]疫情数据异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetBlog():
    try:
        Logger.info(f'[博客接口]正在获取最新文章')
        RawText = requests.get(BlogApi, headers=Headers, timeout=5).text.replace(" ", "").replace("\n", "")
        Urls = re.findall('<h1class="text-default"><aclass="text-default"href="(.*?)">.*?</a></h1>', RawText)
        Titles = re.findall('<h1class="text-default"><aclass="text-default"href=".*?">(.*?)</a></h1>', RawText)
        Data = []
        for i in range(len(Urls)):
            Temp = {
                'title': f'[No.{i+1}]{Titles[i]}',
                'url': Urls[i],
            }
            Data.append(Temp)
        Logger.success(f'[博客接口]获取最新文章成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[博客接口]获取最新文章异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None


def GetCCTVNews(Amount=10):
    try:
        Logger.info(f'[央视新闻接口]正在获取新闻信息')
        with requests.get(CCTVNewsApi, headers=Headers, timeout=5) as Response:
            Response.encoding = Response.apparent_encoding
            RawData = Response.text.strip("news()")
            Result = json.loads(RawData)["data"]["list"]
            Data = []
            for i in range(Amount):
                Temp = {
                    'title': f'[No.{i+1}]{Result[i]["title"]}',
                    'url': Result[i]["url"],
                    'picurl': Result[i]["image"]
                }
                Data.append(Temp)
            Logger.success(f'[央视新闻接口]获取新闻信息成功')
            return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Text = f'[央视新闻接口]获取新闻信息异常,异常信息为:{ExceptionInformation}'
        Logger.error(Text)
        return None
