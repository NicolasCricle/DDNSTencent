import requests

from utils import cfgParse
from tenCentApi import RecordModify


def get_cur_ip(url):
    return requests.get(url=url, timeout=5).json().get("ip")


if __name__ == '__main__':
    ipUrl = cfgParse.get("route", "ip_url")
    ip = cfgParse.get("route", "ip")

    curIp = get_cur_ip(ipUrl)
    if curIp != ip:
        RecordModify(newIp=curIp).run()


