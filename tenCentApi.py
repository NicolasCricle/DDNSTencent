import hmac
import random
import time
from base64 import b64encode
from hashlib import sha1
from urllib import parse
import requests

from utils import cfgParse


class TencentException(Exception):
    pass


class TencentApi:

    def __init__(self, **kwargs):

        data = self.handle_init_params(**kwargs)

        self.params = {
            "Timestamp": TencentApi.get_time_stamp(),
            "Nonce": TencentApi.get_nonce(),
            "SecretId": cfgParse.get("tencent", "secret_id"),
        }
        self.params.update(data)

        scheme = cfgParse.get("tencent", "scheme")
        method = cfgParse.get("tencent", "method")
        netloc = cfgParse.get("tencent", "netloc")
        path = cfgParse.get("tencent", "path")

        sourceStr = TencentApi.generate_source_str(
            method,
            netloc,
            path,
            **self.params
        )
        sign = TencentApi.generate_signature(
            cfgParse.get("tencent", "secret_key"),
            sourceStr
        )

        self.params.update({
            "Signature": sign
        })

        self.url = parse.urlunsplit((scheme, netloc, path, "", ""))

    def handle_init_params(self, **kwargs):
        return kwargs

    @staticmethod
    def get_nonce():
        return str(random.randint(0x0000, 0xFFFF))

    @staticmethod
    def get_time_stamp():
        return str(int(time.time()))

    @staticmethod
    def generate_signature(secretKey, sourceStr):
        hmacCode = hmac.new(secretKey.encode(), sourceStr.encode(), sha1).digest()
        return b64encode(hmacCode).decode()

    @staticmethod
    def generate_source_str(method, netloc, path, **kwargs):
        sourceTuple = sorted(kwargs.items(), key=lambda x: x[0])
        sourceStr = "&".join(["=".join(item) for item in sourceTuple])

        return method + netloc + path + "?" + sourceStr

    @staticmethod
    def send_request(url, params, timeout=10):
        try:
            res = requests.get(url=url, params=params, timeout=timeout)
        except TimeoutError:
            return {
                "code": "8888",
                "message": "timeout error"
            }
        except Exception as e:
            print(e)
            return{
                "code": "9999",
                "message": "some error"
            }

        return res.json()

    def run(self):
        res = TencentApi.send_request(self.url, self.params)
        if res.get("code") != 0:
            raise TencentException(res.get("message"))
        return res.get("data")


class RecordListApi(TencentApi):
    
    def handle_init_params(self, **kwargs):
        data = {
            "Action": "RecordList",
        }
        kwargs.update(data)
        return kwargs


class DomainListApi(TencentApi):
    
    def handle_init_params(self, **kwargs):
        data = {
            "Action": "DomainList"
        }
        kwargs.update(data)

        return kwargs


class RecordModify(TencentApi):

    def handle_init_params(self, **kwargs):

        data = {
            "recordId": kwargs.pop("recordId"),
            "domain": kwargs.pop("domain"),
            "subDomain": kwargs.pop("subDomain"),
            "recordType": kwargs.pop("recordType"),
            "recordLine": kwargs.pop("recordLine"),
            "value": kwargs.pop("value"),
            "Action": "RecordModify"
        }

        kwargs.update(data)
        return kwargs


if __name__ == "__main__":
    ten = RecordModify(newIp="192.168.0.1")
    from pprint import pprint
    pprint(ten.run())



