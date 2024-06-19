# -*- coding: utf-8 -*-
import os

import base64
import datetime
import hashlib
import hmac
import json
import requests
from urllib.parse import urlparse


def parse_url(Url):
    urlInfo = urlparse(Url)
    Host = urlInfo.hostname
    Path = urlInfo.path

    # 签名path不带环境信息
    if Path.startswith(("/release", "/test", "/prepub")):
        Path = "/" + Path[1:].split("/", 1)[1]
    Path = Path if Path else "/"

    # 拼接query参数，query参数需要按字典序排序
    if urlInfo.query:
        queryStr = urlInfo.query
        splitStr = queryStr.split("&")
        splitStr = sorted(splitStr)
        sortStr = "&".join(splitStr)
        Path = Path + "?" + sortStr

    return Host, Path


def get_xdate():
    GMT_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
    xDate = datetime.datetime.utcnow().strftime(GMT_FORMAT)
    return xDate


def sign(Url, HTTPMethod, body, Accept, ContentType):
    ContentMD5 = ""
    # 修改 body 内容
    if HTTPMethod == "POST":
        body = body
        body_json = json.dumps(body)
        body_md5 = hashlib.md5(body_json.encode()).hexdigest()
        ContentMD5 = base64.b64encode(body_md5.encode()).decode()

    xDate = get_xdate()
    Path = parse_url(Url)[1]

    # 获取签名串
    signing_str = "x-date: %s\n%s\n%s\n%s\n%s\n%s" % (
        xDate,
        HTTPMethod,
        Accept,
        ContentType,
        ContentMD5,
        Path,
    )

    # 计算签名
    sign = hmac.new(
        ApiAppSecret.encode(), msg=signing_str.encode(), digestmod=hashlib.sha1
    ).digest()
    sign = base64.b64encode(sign).decode()
    auth = (
        'hmac id="'
        + ApiAppKey
        + '", algorithm="hmac-sha1", headers="x-date", signature="'
    )
    sign = auth + sign + '"'

    return sign


def get_req_headers(Url, HTTPMethod, body, Accept, ContentType):
    headers = {
        "Host": parse_url(Url)[0],
        "Accept": Accept,
        "Content-Type": ContentType,
        "x-date": get_xdate(),
        "Authorization": sign(Url, HTTPMethod, body, Accept, ContentType),
    }

    return headers


def print_req_headers(Url, HTTPMethod, body, Accept, ContentType):
    headers = get_req_headers(Url, HTTPMethod, body, Accept, ContentType)

    for k, v in headers.items():
        print(f"{k}:{v}")

    return None


def request(Url, HTTPMethod, body, Accept, ContentType):
    headers = get_req_headers(Url, HTTPMethod, body, Accept, ContentType)
    body_json = json.dumps(body)

    if HTTPMethod == "GET":
        res = requests.get(Url, headers=headers)
    if HTTPMethod == "POST":
        res = requests.post(Url, headers=headers, data=body_json)

    return res


if __name__ == "__main__":
    # 如果同名环境变量不为空，取环境变量值；否则填写以下值
    API_APP_KEY = ""
    API_APP_SECRET = ""
    API_HOST = ""

    # ApiAppKey = os.getenv("API_APP_KEY", API_APP_KEY)
    # ApiAppSecret = os.getenv("API_APP_SECRET", API_APP_SECRET)
    # if not (ApiAppKey and ApiAppSecret):
    #     raise Exception("ApiAppKey or ApiAppSecret not set.")

    # Set request
    host = os.getenv("API_HOST", API_HOST)

    host = 'https://service-m23z4llz-1258270010.bj.tencentapigw.com.cn/release/'
    ApiAppKey = 'APID5pQwEd993h3tglhi3cnxf3gh2ttkt6i955mc'
    ApiAppSecret='69OQayyrtrk7s0xutQv0jsvS4t3gl58mnfxh1gms'

    path = "/chat"
    Url = host + path
    HTTPMethod = "POST"
    body = {"user_message": "我需要和房东签订什么合同？"}
    Accept = "application/json"
    ContentType = "application/json"

    resonpse = request(
        Url=Url,
        HTTPMethod=HTTPMethod,
        body=body,
        Accept=Accept,
        ContentType=ContentType,
    )

    print(resonpse.text)
    