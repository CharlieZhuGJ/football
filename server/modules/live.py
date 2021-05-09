import json
import urllib
import urllib.request
import pandas as pd


def get_data_by_url(url):
    req = urllib.request.urlopen(url)
    return req.read().decode()


def get_goaldata_jt(url):
    """
    获取基本信息，如进球人员、进球数量
    :param url:
    :return:
    """
    res = {}

    goaldata_jt = get_data_by_url(url)
    data = goaldata_jt.replace("\ufeff", "\r\n").split("\r\nvar ")

    for datum in data:
        if datum:
            kv = datum.split("=")

            res[kv[0].strip()] = kv[1].strip()

    return res


def get_goaldata_js(url):
    """
    获取比赛得分、半场得分
    :param url:
    :return:
    """
    res = {}
    goaldata_js = get_data_by_url(url)
    data = goaldata_js.replace("\ufeff", "\r\n").split("\r\nvar ")

    for datum in data:
        if datum:
            kv = datum.split("=")
            res[kv[0].strip()] = kv[1].strip()
    return res


def get_goaltime(url):
    """
    获取当赛季进球时间统计
    :param url:
    :return:
    """
    res = {}
    goaltime = get_data_by_url(url)
    data = goaltime.replace("\ufeff", "").split("var ")

    for datum in data:
        if datum:
            kv = datum.split("=")
            res[kv[0].strip()] = kv[1].strip()
    return res


def get_lineup_data(url):
    """
    获取比赛球员新
    :param url:
    :return:
    """
    res = {}
    lineup_data = get_data_by_url(url)
    lineup_data = lineup_data.replace("\ufeff", ";\n").split(";\nvar ")

    for datum in lineup_data:
        if datum:
            kv = datum.split("=")
            if kv[0].startswith("HFormation") or kv[0].startswith("VFormation"):
                res.update({kv[0].strip(): kv[1].strip()})
            elif kv[0].startswith("lineup"):
                lineup = json.loads(lineup_data[1].split("=")[1].strip())
                res.update(lineup)
    return res


def get_game_info(url):
    """
    获取比赛基础信息
    :param url:
    :return:
    """
    game_info = get_data_by_url(url)
    res = json.loads(game_info.split("=")[1].strip())
    return res


functions = {
    "goaldata_jt": get_goaldata_jt,
    "goaldata_js": get_goaldata_js,
    "goaltime": get_goaltime,
    "lineupdata": get_lineup_data,
    "gameinfo": get_game_info
}


def main(gid):
    """
    根据gid获取数据
    :param gid:比赛场次编号
    :return:
    """
    urls = {
        "goaldata_jt": "https://data.7m.com.cn/goaldata/jt/4074/{}.js".format(gid),
        "goaldata_js": "https://data.7m.com.cn/goaldata/js/4074/{}.js".format(gid),
        "goaltime": "https://data.7m.com.cn/goaldata/goaltime_stat/{}.js".format(gid),
        "lineupdata": "https://wlive-js.7m.com.cn/lineupdata/gb/{}.js".format(gid),
        "gameinfo": "https://analyse.7m.com.cn/{}/data/gameinfo_gb.js".format(gid)
    }

    results = {}
    for k, v in urls.items():
        result = functions[k](v)
        print(result)
        results.update(result)
    df = pd.DataFrame.from_dict(results, orient='index')
    df = df.transpose()
    print(df)
    df.to_csv(gid + '{}.csv'.format("_live"), encoding="utf_8_sig")


if __name__ == "__main__":
    # {'GameId': '4074677', 'StartTime': '2021-05-02 23:59:00', 'CompetitionId': '34', 'CompetitionColor': '006EF0',
    # 'CompetitionName': '意甲', 'HomeId': '54', 'HomeName': '乌迪内斯', 'AwayId': '2', 'AwayName': '尤文图斯'}

    # {'GameId': '4073142', 'StartTime': '2021-05-03 03:00:00', 'CompetitionId': '85', 'CompetitionColor': '993300',
    # 'CompetitionName': '西甲', 'HomeId': '350', 'HomeName': '巴伦西亚', 'AwayId': '514', 'AwayName': '巴塞罗那'}
    main('4074674')
