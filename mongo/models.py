#!/usr/bin/python
# _*_ coding: utf-8 _*_

# Create your models here.
from mongoengine import *

class NginxAccessRecord(DynamicDocument):
    """nginx 访问日志记录
    """
    host = StringField()
    user = StringField() 
    method = StringField()
    path = StringField()
    code = IntField()
    size = IntField()
    referer = StringField()
    agent = StringField()
    time = DateTimeField()

class Ip(DynamicDocument):
    """访问IP详细信息
    使用baiduApi获取ip地址位置
    ip 设为unique索引

    例子：
    curl  --get --swebapi/iplocation?ip=220.181.111.188'  -H 'apikey:bcce1190dfb38748afbc2ca5df311a70'
    {
    "errNum":0,
    "retMsg":"success",
    "retData":{
        "address":"CN|北京|北京|None|CHINANET|0|0",
        "content":{
            "address_detail":{
                "province":"北京市",
                "city":"北京市",
                "district":"",
                "street":"",
                "street_number":"",
                "city_code":131
            },
            "address":"北京市",
            "point":{
                "y":"4825907.72",
                "x":"12958160.97"
            }
        },
        "status":0
    }
    """
    ip = StringField()
    longitude = FloatField()
    latitude = FloatField()
    visit_num = IntField()
    city_code = IntField()
    # 详细地址信息
    privince = StringField()
    city = StringField()
    district = StringField()
    street = StringField()
    street_number = StringField()

class Os(DynamicDocument):
    """操作系统记录
    name 设为unique索引
    """
    name = StringField()
    visit_num = IntField()

class Browser(DynamicDocument):
    """浏览器记录
    name 设为unique索引
    """
    name = StringField()
    visit_num = IntField()

class UrlPath(DynamicDocument):
    """被请求最多链接
    name 设为unique索引
    """
    name = StringField()
    visit_num = IntField()

class DayVisit(DynamicDocument):
    """每天访问量
    """
    date = StringField()
    visit_num = IntField()
