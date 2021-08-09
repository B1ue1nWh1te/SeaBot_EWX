from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask, jsonify, request
import json
import sys

from Ability import *
import Logger


# 初始化
try:
    Logger.Log("[API服务初始化]正在加载配置")
    with open("Setting.json", "r", encoding="utf-8") as f:
        Setting = json.load(f)

    # API服务配置
    Host = Setting["Api"]["Host"]
    Port = Setting["Api"]["Port"]
    app = Flask(__name__)

    Logger.Log("[API服务初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[API服务初始化异常]异常信息为:{}".format(ExceptionInformation)
    Logger.Log(Text)
    sys.exit(0)


# 天气接口
@app.route('/weather/', methods=['GET'])
def Weather():
    City = request.args.get("city")
    result = GetWeather(City)
    return jsonify(result)


# B站排行榜接口
@app.route('/bilibili/', methods=['GET'])
def Bilibili():
    Type = request.args.get("type")
    Amount = request.args.get("amount", 10)
    result = GetBilibiliRank(Type, int(Amount))
    return jsonify(result)


# 微博排行榜接口
@app.route('/weibo/', methods=['GET'])
def Weibo():
    Type = request.args.get("type")
    Amount = request.args.get("amount", 10)
    result = GetWeiboRank(Type, int(Amount))
    return jsonify(result)


# 知乎热榜接口
@app.route('/zhihu/', methods=['GET'])
def Zhihu():
    Amount = request.args.get("amount", 10)
    result = GetZhihuRank(int(Amount))
    return jsonify(result)


# 同花顺快讯接口
@app.route('/tonghuashun/', methods=['GET'])
def Tonghuashun():
    result = GetTonghuashunNews()
    return jsonify(result)


# 网易云音乐排行榜接口
@app.route('/wangyiyun/', methods=['GET'])
def Wangyiyun():
    Type = request.args.get("type")
    result = GetWangyiyunRank(Type, 10)
    return jsonify(result)


# 国内疫情数据接口
@app.route('/epidemic/', methods=['GET'])
def Epidemic():
    Province = request.args.get("province")
    result = GetEpidemicData(Province)
    return jsonify(result)


# 博客接口
@app.route('/blog/', methods=['GET'])
def Blog():
    result = GetBlog()
    return jsonify(result)


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=5000, use_reloader=True, debug=True)
    WSGIServer((Host, Port), app).serve_forever()
