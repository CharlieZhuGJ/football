import json
import time
import urllib
import urllib.request
from server.modules.live import main as live
from server.modules.analysis import main as analysis
from server.modules.information import main as information


def get_data_by_url(url):
    req = urllib.request.urlopen(url)
    return req.read().decode()


def main(date):
    report = "http://report.7m.com.cn/data/list/gb/{}.js".format(date)

    comp_list = get_data_by_url(report)
    comp_list = json.loads(comp_list.split(" = ")[1][:-1])

    for comp in comp_list:
        gid = comp['GameId']
        print(gid)
        live(gid)
        analysis(gid)
        information(gid)
        time.sleep(5)


if __name__ == "__main__":
    # {'GameId': '4074677', 'StartTime': '2021-05-02 23:59:00', 'CompetitionId': '34', 'CompetitionColor': '006EF0',
    # 'CompetitionName': '意甲', 'HomeId': '54', 'HomeName': '乌迪内斯', 'AwayId': '2', 'AwayName': '尤文图斯'}

    # {'GameId': '4073142', 'StartTime': '2021-05-03 03:00:00', 'CompetitionId': '85', 'CompetitionColor': '993300',
    # 'CompetitionName': '西甲', 'HomeId': '350', 'HomeName': '巴伦西亚', 'AwayId': '514', 'AwayName': '巴塞罗那'}
    main('2021-05-02')
