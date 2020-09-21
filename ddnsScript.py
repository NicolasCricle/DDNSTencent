import requests

from utils import cfgParse
from tenCentApi import RecordModify, DomainListApi, RecordListApi


def get_cur_ip(url):
    return requests.get(url=url, timeout=5).json().get("ip")


def main():
    ipUrl = cfgParse.get("route", "ip_url")
    oldIp = cfgParse.get("route", "ip")
    curIp = get_cur_ip(ipUrl)
    if curIp == oldIp:
        return
    data = DomainListApi().run()
    domains = data.get("domains")
    for item in domains:
        recordLis = RecordListApi(domain=item["name"]).run()
        domain = recordLis.get("domain")
        records = recordLis.get("records")


        for record in records:
            sub_domain = record.get("name")
            if sub_domain == "@":
                continue

            RecordModify(
                recordId=record.get("id"),
                domain=domain,
                subDomain=record.get("name"),
                recordLine=record.get("line"),
                recordType=record.get("type"),
                value=curIp
            ).run()

    else:
        cfgParse.set("route", "ip", curIp)

if __name__ == '__main__':
    main()
