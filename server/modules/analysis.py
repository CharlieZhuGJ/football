import json
import urllib
import urllib.request
import pandas as pd


def get_data_by_url(url):
    req = urllib.request.urlopen(url)
    return req.read().decode()


def get_game_info(url):
    """
    获取比赛信息
    :param url:
    :return:
    """
    info = get_data_by_url(url)
    res = json.loads(info.split("=")[1].strip())
    return res


def get_game_history(url):
    """
    获取对阵双方历史比赛信息
    :param url:
    :return:
    """
    history = get_data_by_url(url)
    res = json.loads(history.split('=')[1].strip())
    return res


def get_game_team_history(url):
    """
    获取对阵双方过去场次信息
    :param url:
    :return:
    """
    team_history = get_data_by_url(url)
    res = json.loads(team_history.split('=')[1].strip())
    return res


def get_game_team_stats(url):
    """
    获取比赛统计信息
    :param url:
    :return:
    """
    team_stats = get_data_by_url(url)
    res = json.loads(team_stats.split('=')[1].strip())
    return res


def get_game_team_fixture(url):
    """
    获取比赛结构信息
    :param url:
    :return:
    """
    team_fixture = get_data_by_url(url)
    res = json.loads(team_fixture.split('=')[1].strip())
    return res


def get_game_prediction(url):
    """
    获取比赛预测信息
    :param url:
    :return:
    """
    res = {}
    prediction = get_data_by_url(url)
    ss = prediction.split(' = ')[1][1:-1].strip()
    ss = ss.replace("\'", "")
    ss = ss.split(',')

    for s in ss:
        s = s.replace('<span class="o_l">', "")
        s = s.replace('<span class="o_w">', "")
        s = s.replace('<span class="o_d">', "")
        s = s.replace('</span>', " ")
        s = s.replace('<font color="FF0000">', "")
        s = s.replace('<font color="0000FF">', "")
        s = s.replace('<font color="006600">', "")
        s = s.replace('</font>', " ")
        kv = s.split(":")
        res[kv[0]] = kv[1]

    return res


def get_game_lineup(url):
    """
    获取比赛球员信息
    :param url:
    :return:
    """
    lineup = get_data_by_url(url)
    lineup = lineup.split("=")[1].strip().replace("'", "\"")
    res = json.loads(lineup)
    return res


def get_game_standings(url):
    """
    获取standing信息
    :param url:
    :return:
    """
    standings = get_data_by_url(url)
    res = json.loads(standings.split("=")[1].strip())
    return res


def get_game_oddsway(url):
    """
    获取赔率信息
    :param url:
    :return:
    """
    oddsway = get_data_by_url(url)
    res = json.loads(oddsway.split("=")[1].strip())
    return res


functions = {
    "gameinfo": get_game_info,
    "gamehistory": get_game_history,
    "gameteamhistory": get_game_team_history,
    "gameteamstats": get_game_team_stats,
    "gameteamfixture": get_game_team_fixture,
    "gameprediction": get_game_prediction,
    "gamelineup": get_game_lineup,
    "gamestandings": get_game_standings,
    "gameoddsway": get_game_oddsway,
}


def main(gid):
    """
    根据gid获取数据
    :param gid:比赛场次编号
    :return:
    """
    urls = {
        "gameinfo": "http://analyse.7m.com.cn/{}/data/gameinfo_gb.js".format(gid),
        "gamehistory": "http://analyse.7m.com.cn/{}/data/gamehistory_gb.js".format(gid),
        "gameteamhistory": "http://analyse.7m.com.cn/{}/data/gameteamhistory_gb.js".format(gid),
        "gameteamstats": "http://analyse.7m.com.cn/{}/data/gameteamstats_gb.js".format(gid),
        "gameteamfixture": "http://analyse.7m.com.cn/{}/data/gameteamfixture_gb.js".format(gid),
        "gameprediction": "http://analyse.7m.com.cn/{}/data/gameprediction_gb.js".format(gid),
        "gamelineup": "http://analyse.7m.com.cn/{}/data/gamelineup_gb.js".format(gid),
        "gamestandings": "http://analyse.7m.com.cn/{}/data/gamestandings_gb.js".format(gid),
        "gameoddsway": "http://analyse.7m.com.cn/{}/data/gameoddsway_gb.js".format(gid),
    }
    results = {}
    for k, v in urls.items():
        result = functions[k](v)
        print(result)
        results.update(result)
    df = pd.DataFrame.from_dict(results, orient='index')
    df = df.transpose()
    print(df)
    df.to_csv(gid + '{}.csv'.format("_analysis"), encoding="utf_8_sig")


if __name__ == "__main__":
    # {'GameId': '4074677', 'StartTime': '2021-05-02 23:59:00', 'CompetitionId': '34', 'CompetitionColor': '006EF0',
    # 'CompetitionName': '意甲', 'HomeId': '54', 'HomeName': '乌迪内斯', 'AwayId': '2', 'AwayName': '尤文图斯'}

    # {'GameId': '4073142', 'StartTime': '2021-05-03 03:00:00', 'CompetitionId': '85', 'CompetitionColor': '993300',
    # 'CompetitionName': '西甲', 'HomeId': '350', 'HomeName': '巴伦西亚', 'AwayId': '514', 'AwayName': '巴塞罗那'}
    main('4064251')
