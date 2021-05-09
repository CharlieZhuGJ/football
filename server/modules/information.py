import json
import urllib
import urllib.request
import pandas as pd


def get_data_by_url(url):
    req = urllib.request.urlopen(url)
    # print(req.read().decode())
    return req.read().decode()


def get_news(url):
    """
    获取本场比赛相关新闻
    :param url:
    :return:
    """
    res = {}
    analyse_news = get_data_by_url(url)
    analyse_news = json.loads(analyse_news.split("=")[1][:-1])
    for new in analyse_news:
        res.update(new)
    return res


def get_reviews(url):
    """
    获取本场比赛战意分析
    :param url:
    :return:
    """
    reviews = get_data_by_url(url)
    reviews = ";\n" + reviews
    res = {}
    for item in reviews.split(";\nvar "):
        if item:
            kv = item.split("=")
            key = kv[0].strip()
            val = kv[1].strip()
            if val.endswith(";"):
                val = val[:-1]
            res[key] = json.loads(val)

    return res


def get_injure(url):
    """
    获取伤停相关信息
    :param url:
    :return:
    """
    res = {}
    try:
        injures = get_data_by_url(url)
        injures = injures.replace("\ufeff", "\r\n").split("\r\nvar ")

        for injure in injures:
            if injure:
                kv = injure.split("=")
                key = kv[0].strip()
                val = kv[1].strip().split(";")[0]
                res[key] = val
    except Exception:
        print("injures access failed")
    return res


def get_crowns(url):
    """

    :param url:
    :return:
    """
    res = {}
    try:
        crowns = get_data_by_url(url)
        res = json.loads(crowns.split("=")[1][:-1])
    except Exception:
        print("crowns access failed")
    return res


def get_lottery(url):
    """
    获取博彩赔率相关信息
    :param url:
    :return:
    """
    res = {}
    try:
        lottery = get_data_by_url(url)
        res = json.loads(lottery.split("= ")[1])
    except Exception:
        print("lottery access failed")
    return res


functions = {
    "news": get_news,
    "reviews": get_reviews,
    "injure": get_injure,
    "crowns": get_crowns,
    "lottery": get_lottery,
}


def main(gid):
    """
    根据gid获取数据
    :param gid:比赛场次编号
    :return:
    """
    urls = {
        "news": "http://news.7m.com.cn/data/game/{}_json.js".format(gid),
        "reviews": "http://report.7m.com.cn/data/game/gb/{}.js".format(gid),
        "injure": "http://data.7m.com.cn/analyse/gb/nline_up_injure/{}.js".format(gid),
        "crowns": "http://crowns2.7m.com.cn/report/{}.js".format(gid),
        "lottery": "http://data.lottery.7m.com.cn/data/{}.js".format(gid),
    }

    results = {}
    for k, v in urls.items():
        result = functions[k](v)
        print(result)
        results.update(result)
    df = pd.DataFrame.from_dict(results, orient='index')
    df = df.transpose()
    print(df)
    df.to_csv(gid + '{}.csv'.format("_information"), encoding="utf_8_sig")


if __name__ == "__main__":
    # {'GameId': '4074677', 'StartTime': '2021-05-02 23:59:00', 'CompetitionId': '34', 'CompetitionColor': '006EF0',
    # 'CompetitionName': '意甲', 'HomeId': '54', 'HomeName': '乌迪内斯', 'AwayId': '2', 'AwayName': '尤文图斯'}

    # {'GameId': '4073142', 'StartTime': '2021-05-03 03:00:00', 'CompetitionId': '85', 'CompetitionColor': '993300',
    # 'CompetitionName': '西甲', 'HomeId': '350', 'HomeName': '巴伦西亚', 'AwayId': '514', 'AwayName': '巴塞罗那'}
    main('4074674')


