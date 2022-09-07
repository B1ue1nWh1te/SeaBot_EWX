import re
import sys
import json
import requests
import Log


try:
    Log.info("[服务功能初始化]正在加载配置")
    with open("setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)["Ability"]
    Headers = Setting["Headers"]
    WeiboRankApi = Setting["WeiboRankApi"]
    ZhihuRankApi = Setting["ZhihuRankApi"]
    ZhihuQuestionApi = Setting["ZhihuQuestionApi"]
    CCTVNewsApi = Setting["CCTVNewsApi"]
    TonghuashunApi = Setting["TonghuashunApi"]
    LeetcodeApi = Setting["LeetcodeApi"]
    LeetcodeProblemApi = Setting["LeetcodeProblemApi"]
    Log.success("[服务功能初始化][成功]配置加载完成")
except Exception:
    ExceptionInformation = sys.exc_info()
    Log.error(f'[服务功能初始化][失败]异常信息为:{ExceptionInformation}')
    sys.exit()


def GetWeiboRank() -> list:
    try:
        global Headers, WeiboRankApi
        Log.info("[服务功能][微博热搜]正在获取微博热搜榜信息")
        Data = []
        RawData = requests.get(WeiboRankApi, headers=Headers, timeout=5).json()
        Result = RawData["data"]["band_list"]
        for i in range(10):
            Temp = {
                'title': f'[No.{i+1}]{Result[i]["note"]}',
                'url': f'https://s.weibo.com/weibo?q=%23{Result[i]["note"]}%23'
            }
            Data.append(Temp)
        Log.success(f'[服务功能][微博热搜]获取微博热搜榜信息成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[服务功能][微博热搜]获取微博热搜榜信息异常，异常信息为:{ExceptionInformation}')
        return None


def GetZhihuRank() -> list:
    try:
        global Headers, ZhihuRankApi, ZhihuQuestionApi
        Log.info("[服务功能][知乎热榜]正在获取知乎热榜信息")
        Data = []
        RawData = requests.get(ZhihuRankApi, headers=Headers, timeout=5).json()["data"]
        for i in range(10):
            Temp = {
                'title': f'[No.{i+1}]{RawData[i]["target"]["title"]}',
                'url': f'{ZhihuQuestionApi}{RawData[i]["target"]["id"]}',
                'picurl': RawData[i]["children"][0]["thumbnail"]
            }
            Data.append(Temp)
        Log.success("[服务功能][知乎热榜]获取知乎热榜信息成功")
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[服务功能][知乎热榜]获取知乎热榜信息异常，异常信息为:{ExceptionInformation}')
        return None


def GetCCTVNews() -> list:
    try:
        global Headers, CCTVNewsApi
        Log.info(f'[服务功能][央视新闻]正在获取央视新闻信息')
        Data = []
        Response = requests.get(CCTVNewsApi, headers=Headers, timeout=5)
        Response.encoding = Response.apparent_encoding
        RawData = Response.text.strip("news()")
        Result = json.loads(RawData)["data"]["list"]
        for i in range(10):
            Temp = {
                'title': f'[No.{i+1}]{Result[i]["title"]}',
                'url': Result[i]["url"],
                'picurl': Result[i]["image"]
            }
            Data.append(Temp)
        Log.success(f'[服务功能][央视新闻]获取央视新闻信息成功')
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[服务功能][央视新闻]获取央视新闻信息异常，异常信息为:{ExceptionInformation}')
        return None


def GetTonghuashunNews() -> list:
    try:
        global Headers, TonghuashunApi
        Log.info("[服务功能][同花顺快讯]正在获取同花顺快讯信息")
        Data = []
        RawData = requests.get(TonghuashunApi, headers=Headers, timeout=5).json()["data"]["list"]
        for i in range(10):
            Temp = {
                'title': f'[No.{i+1}]{RawData[i]["title"]}',
                'url': RawData[i]["appUrl"]
            }
            Data.append(Temp)
        Log.success("[服务功能][同花顺快讯]获取同花顺快讯信息成功")
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[服务功能][同花顺快讯]获取同花顺快讯信息异常，异常信息为:{ExceptionInformation}')
        return None


def GetLeetcodeEveryday() -> str:
    from html import unescape
    try:
        global Headers, LeetcodeApi, LeetcodeProblemApi
        Log.info("[服务功能][Leetcode每日一题]正在获取Leetcode每日一题信息")
        headers = Headers
        headers["origin"] = "https://leetcode-cn.com"
        data = {"operationName": "questionOfToday", "variables": {
        }, "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"}
        RawData = requests.post(LeetcodeApi, json=data, headers=headers, timeout=5).json()
        EnglishTitle = RawData["data"]["todayRecord"][0]["question"]["questionTitleSlug"]
        QuestionUrl = f"{LeetcodeProblemApi}{EnglishTitle}"
        data = {"operationName": "questionData", "variables": {"titleSlug": EnglishTitle}, "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"}
        RawData = requests.post(LeetcodeApi, json=data, headers=headers, timeout=5).json()
        Data = RawData["data"]["question"]
        ID = Data["questionFrontendId"]
        Difficulty = Data["difficulty"]
        ChineseTitle = Data["translatedTitle"]
        Content = unescape(Data["translatedContent"])
        Content = re.sub(r"(<\w+>|</\w+>)", "", Content).replace("\t", "").replace("\n\n", "\n").replace("\n\n", "\n")
        Data = f"[题目]{ID}.{ChineseTitle}\n[难度]{Difficulty}\n[内容]\n{Content}\n[链接]{QuestionUrl}"
        Log.success("[服务功能][Leetcode每日一题]获取Leetcode每日一题信息成功")
        return Data
    except Exception:
        ExceptionInformation = sys.exc_info()
        Log.error(f'[服务功能][Leetcode每日一题]获取Leetcode每日一题信息异常，异常信息为:{ExceptionInformation}')
        return None
