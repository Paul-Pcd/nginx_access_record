#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
import json
import models
import urllib2
from mongoengine import *

# 连接至mongoDB, 选择access_record数据库
connect('access_record', host = '127.0.0.1', port=12345)

def get_os_name(agent_info):
    """从agent信息中解析出操作系统名字

    Args:
        agent_info: string 
        例子: 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MX4 Pro Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
    """
    if not agent_info:
        raise Exception('agent_info is None in mongo_engine.get_os_name')

    # GET "Macintosh; Inter Mac OS X 10.11; rv:42.0"
    pattern = re.compile(r'\(.+?\)')
    os_info_list = pattern.findall(agent_info)
    if not os_info_list:
        return 'UNKNOWN OS'
    # GET "Macintosh_Inter_Mac_OS_X_10.11_rv:42.0"
    os_info = '_'.join(re.split('[,; ]', os_info_list[0])).replace('__', '_')
    return os_info

def get_browser_name(agent_info):
    """从agent信息中解析出浏览器名字

    Args:
        agent_info: string 
        例子: 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; MX4 Pro Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    """
    if not agent_info:
        raise Exception('agent_info is None in mongo_engine.get_browser_name')

    agent_info = agent_info.lower()

    if agent_info.find('chrome') != -1:
        return 'Chrome'
    elif agent_info.find('firefox') != -1:
        return 'Firefox'
    elif agent_info.find('safiri') != -1:
        return 'Safiri'
    else:
        return agent_info.split(' ')[-1].split('/')[0]


def get_ip_location_info(ip):
    """获取ip的地理信息
    
    Args:
        ip: string 例子: '14.233.34.23'

    Return:
        {
            'city_code': 131,
            'longtitude': 90,
            'latitude': 80,
        }
    """
    url = "http://apis.baidu.com/apistore/lbswebapi/iplocation?coor=bd09ll&ip={ip}".format(ip=ip)

    req = urllib2.Request(url)
    req.add_header("apikey", " bcce1190dfb38748afbc2ca5df311a70")

    ip_location = urllib2.urlopen(req).read()
    ip_location = json.loads(ip_location)

    if not ip_location or ip_location['errNum'] != 0:
        raise Exception('fail to get ip location in mongo_engine.get_ip_location_info')

    return {
    'city_code': ip_location['retData']['content']['address_detail']['city_code'],
    'city_name': ip_location['retData']['address'],
    'longitude': ip_location['retData']['content']['point']['x'],
    'latitude': ip_location['retData']['content']['point']['y'],
    }

def process_total_nginx_access_log():
    """处理全量nginx_access_log

    数据库: access_record 
    集合: nginx_access_log
    日志格式:
    {
        "_id":"564fcecb83fcecae86000001",
        "host":"127.0.0.1",
        "user":"-",
        "method":"GET",
        "path":"/",
        "code":"200",
        "size":"90827",
        "referer":"-",
        "agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0",
        "time":"2015-11-21 01:54:18"
    }
    """
    city_info = {}
    os_info = {}
    browser_info = {}
    url_path_info = {}
    day_visit_info = {}
    total_visit_num = 0
    for access_record in  models.NginxAccessRecord.objects:
        # 获取ip信息
        ip = access_record.host
        city_location = get_ip_location_info(ip)
        city_id = str(city_location['city_id'])

        if city_id in city_info.keys():
            city_info[city_id]['visit_num'] += 1
        else:    
            city_info[city_id] = {
            'longitude':city_location['longitude'],
            'latitude':city_location['latitude'],
            'visit_num': 1,
            }

        # 获取操作系统信息
        os_name = get_os_name(access_record.agent)
        os_info[os_name] = 1 if os_name not in os_info.keys() else os_info[os_name] + 1

        # 获取浏览器信息
        browser_name = get_browser_name(access_record.agent)
        browser_info[browser_name] = 1 if browser_name not in browser_info.keys() else browser_info[browser_name] + 1

        # 获取URL_PATH信息
        url_path_name = access_record.path
        url_path_info[url_path_name] = 1 if url_path_name not in url_path_info.keys() else url_path_info[url_path_name] + 1

        # 获取每日访问信息
        date = access_record.time.strftime('%Y-%m-%d %H:%M%S').split(' ')[0]
        day_visit_info[date] = 1 if date not in day_visit_info.keys() else day_visit_info[date] + 1

        # 总访问量
        total_visit_num += 1
 
    print city_info
    print os_info
    print browser_info
    print url_path_info
    print day_visit_info
    print total_visit_num

def get_city_info():
    """获取客户端ip信息

    return:
        [] 例子:
    """
    pass

def get_day_visit_info():
    """获取每天访问量数据

    return:
        {} 例子:
        { 
            'date':['11-10','11-11','11-12','11-13','11-14'],
            'visit_num':[20, 10, 15, 30, 20]
        }   
    """
    pass

def get_os_info():
    """获取客户端操作系统分布

    return:
        {} 例子:
        {
            'name': ['Mac OS', 'Windows 10', 'Linux'],
            'visit_num': [100, 500, 1000],
        }
    """
    pass

def get_browser_info():
    """获取客户端浏览器分布

    return:
        {} 例子:
        {
            'name': ['Firefox', 'Chrome', 'Safiri'],
            'visit_num': [100, 500, 1000],
        }
    """
    pass

def get_url_path_info():
    """获取热门文章列表

    return:
        {} 例子:
        {
            'name': ['Pythonic', '点滴', 'Linux命令行'],
            'visit_num': [100, 500, 1000],
        }
    """
    pass

def get_total_visit_num_info():
    """返回总访问次数

    return:
        int
    """
    pass

if __name__ == '__main__':
    process_total_nginx_access_log()
    # print get_ip_location_info("121.41.119.102")
