#!/usr/bin/python
# _*_ coding:utf-8 _*_

import re
import sys
import json
import random
import models
import urllib2
import MySQLdb
from mongoengine import *

# 连接至mongoDB, 选择access_record数据库
# connect('access_record', host = '127.0.0.1', port=12345)
connect('access_record', host = 'chenhuan0103.com', port=12345)

class GetArticleNameError(Exception):
    """获取Article名字失败
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ProcessNginxLogError(Exception):
    """解析Nginx日志错误异常
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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
        raise ProcessNginxLogError('agent_info is None in mongo_engine.get_os_name')

    # GET "Macintosh; Inter Mac OS X 10.11; rv:42.0"
    pattern = re.compile(r'\((.+?)\)')
    os_info_list = pattern.findall(agent_info)
    if not os_info_list:
        raise ProcessNginxLogError("no OS info in {agent_info}".format(agent_info=agent_info))

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
        raise ProcessNginxLogError('agent_info is None in mongo_engine.get_browser_name')

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
        raise ProcessNginxLogError("fail to get {ip} location in mongo_engine.get_ip_location_info".format(ip=ip))

    return {
    'city_code': ip_location['retData']['content']['address_detail']['city_code'],
    'city_name': ip_location['retData']['address'],
    'longitude': ip_location['retData']['content']['point']['x'],
    'latitude': ip_location['retData']['content']['point']['y'],
    }

def get_article_title(article_id):
    """根据article_id获取article名字

    Args:
        article_id: int

    Returns:
        article_name: string
    """
    conn = MySQLdb.connect(host="chenhuan0103.com", user="root", passwd="123456", db="blog", charset="utf8")
    cursor = conn.cursor() 

    sql = "SELECT title from hachi_article WHERE id={article_id}".format(article_id=article_id)
    cursor.execute(sql)
    article_title = cursor.fetchone()

    if not article_title:
        raise GetArticleNameError('article_id={id} not exist'.format(id=article_id))

    conn.close()
    return article_title[0]

def process_nginx_access_log():
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
    location_info = {}
    os_info = {}
    browser_info = {}
    url_path_info = {}
    day_visit_info = {}
    total_visit_num = 0

    for access_record in  models.NginxAccessRecord.objects:
        try:
            if access_record.host == '127.0.0.1':
                continue
            if access_record.agent.find('Baiduspider') != -1:
                continue
            if access_record.agent.find('Googlebot') != -1:
                continue
            pattern = re.compile(r'.+articleFront/view&id=.+')
            print access_record.path
            if not access_record.path or not pattern.match(access_record.path):
                continue

            # 获取URL_PATH信息
            url_path_name = access_record.path
            article_id = url_path_name.split("=")[-1]
            article_title = get_article_title(article_id)
            url_path_info[article_title] = 1 if article_title not in url_path_info.keys() else url_path_info[article_title] + 1

            # 获取ip位置信息
            ip = access_record.host
            city_location = get_ip_location_info(ip)
            city_code = str(city_location['city_code'])

            if city_code in location_info.keys():
                location_info[city_code]['visit_num'] += 1
            else:    
                location_info[city_code] = {
                'longitude':float(city_location['longitude']),
                'latitude':float(city_location['latitude']),
                'visit_num': 1,
                }

            # 获取操作系统信息
            os_name = get_os_name(access_record.agent)
            os_info[os_name] = 1 if os_name not in os_info.keys() else os_info[os_name] + 1

            # 获取浏览器信息
            browser_name = get_browser_name(access_record.agent)
            browser_info[browser_name] = 1 if browser_name not in browser_info.keys() else browser_info[browser_name] + 1

            # 获取每日访问信息
            date = access_record.time.strftime('%Y-%m-%d %H:%M%S').split(' ')[0]
            day_visit_info[date] = 1 if date not in day_visit_info.keys() else day_visit_info[date] + 1

            # 总访问量
            total_visit_num += 1
        except ProcessNginxLogError, error:
            pass

    return {
    'location_info': location_info,
    'os_info': os_info,
    'browser_info': browser_info,
    'url_path_info': url_path_info,
    'day_visit_info': day_visit_info,
    'total_visit_num': total_visit_num,
    }

def format_access_info(access_info):
    """格式化访问信息, 供ECHart展示

    Args:
        {} 例子
        {
            "browser_info":{
                "Chrome":15,
                "Firefox":6
            },
            "day_visit_info":{
                "2015-11-20":2,
                "2015-11-21":2,
                "2015-11-22":17
            },
            "location_info":{
                "16":{
                    "latitude":"26.05011830",
                    "visit_num":21,
                    "longitude":"117.98494312"
                }
            },
            "url_path_info":{
                "/blog/index.php?r=catalogueFront/articles&id=10":2,
                "/blog/assets/css/guai_blog.css":2,
                "/blog/index.php?r=tagFront/articles&id=7":2,
                "/blog/assets/2cdcf402/pager.css":2,
                "/blog/index.php?r=admin/admin/index":13
            },
            "total_visit_num":21,
            "os_info":{
                "(Macintosh_Intel_Mac_OS_X_10.11_rv:42.0)":6,
                "(Macintosh_Intel_Mac_OS_X_10_11_1)":15
            }
        }

    Return:
        {
            "browser_info":{
                "name": ['Chrome', 'Firefox'],
                "visit_num": [15, 6],
            },
            "day_visit_info":{
                "date": ['2015-11-20', '2015-11-21', '2015-11-22'],
                "visit_num": [2, 2, 17],
            },
            "location_info":{
                "16":{
                    "latitude":"26.05011830",
                    "visit_num":21,
                    "longitude":"117.98494312"
                }
            },
            "url_path_info":{
                "name": [
                "/blog/index.php?r=catalogueFront/articles&id=10",
                "/blog/assets/css/guai_blog.css",
                "/blog/index.php?r=tagFront/articles&id=7",
                "/blog/assets/2cdcf402/pager.css",
                "/blog/index.php?r=admin/admin/index",
                ],
                "visit_num": [2, 2, 2, 2, 13],
            },
            "os_info":{
                "name": [
                "(Macintosh_Intel_Mac_OS_X_10.11_rv:42.0)",
                "(Macintosh_Intel_Mac_OS_X_10_11_1)",
                ]
                "visit_num": [6, 15],
            }
            "total_visit_num":21,
        }
    """
    if not access_info:
        raise Exception('access_info is None in mongo_engine.format_access_info')

    access_info_echart = {}

    # ip_location_info
    # {
    #     'name': '西安',
    #     'value':  20,
    #     'geoCoord': [117.27, 31.86],
    # }
    access_info_echart['location_info'] = []
    for city_code,location_info in access_info['location_info'].items():
        access_info_echart['location_info'].append({
            'name': str(city_code),
            'value': location_info['visit_num'],
            'geoCoord': [location_info['longitude'], location_info['latitude']],
            })

    # os_info
    os_name_list = []
    os_visit_num_list = []
    # 对操作系统按照visit_num从小到大排序
    os_info = access_info['os_info']
    os_info = sorted(os_info.iteritems(), key=lambda d:d[1], reverse=False)
    for (name,visit_num) in os_info:
        os_name_list.append(name)
        os_visit_num_list.append(visit_num)
    access_info_echart['os_info'] = {
    'name': os_name_list,
    'visit_num': os_visit_num_list,
    }

    # browser
    browser_name_list = []
    browser_visit_num_list = []
    # 对browser按visit_num排序, 从小到大
    browser_info = access_info['browser_info']
    browser_info = sorted(browser_info.iteritems(), key=lambda d:d[1], reverse=False)
    for (name,visit_num) in browser_info:
        browser_name_list.append(name)
        browser_visit_num_list.append(visit_num)
    access_info_echart['browser_info'] = {
    'name': browser_name_list,
    'visit_num': browser_visit_num_list,
    }

    # url_path
    url_path_name_list = []
    url_path_visit_num_list = []
    # 对url_path_info按visti_num排序,从小到大
    url_path_info = access_info['url_path_info']
    url_path_info = sorted(url_path_info.iteritems(), key=lambda d:d[1], reverse=False)
    for (name,visit_num) in url_path_info:
        url_path_name_list.append(name)
        url_path_visit_num_list.append(visit_num)
    access_info_echart['url_path_info'] = {
    'name': url_path_name_list,
    'visit_num': url_path_visit_num_list,
    }

    # day_visit
    date_list = []
    visit_num_list = []
    for date,visit_num in access_info['day_visit_info'].items():
        date_list.append(date)
        visit_num_list.append(visit_num)
    access_info_echart['day_visit_info'] = {
    'date': date_list,
    'visit_num': visit_num_list,
    }

    # total_visit_num
    access_info_echart['total_visit_num'] = access_info['total_visit_num']

    return access_info_echart

def get_access_info():
    """返回用户访问信息
    """
    access_info = process_nginx_access_log()
    return format_access_info(access_info)

def test_process_nginx_access_log():
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
    location_info = {}
    os_info = {}
    browser_info = {}
    url_path_info = {}
    day_visit_info = {}
    total_visit_num = 0

    for access_record in  models.NginxAccessRecord.objects:
        try:
            # 获取URL_PATH信息
            url_path_name = access_record.path
            # URL=index.php?r=articleFront/view&id=才有效
            pattern = re.compile(r'.+articleFront/view&id=.+')
            if not pattern.match(url_path_name):
                continue

            article_id = url_path_name.split("=")[-1]
            article_title = get_article_title(article_id)
            url_path_info[article_title] = 1 if article_title not in url_path_info.keys() else url_path_info[article_title] + 1

            # 获取ip位置信息
            ip = access_record.host
            if ip == '127.0.0.1':
                continue

            print access_record.agent
            continue

            city_location = get_ip_location_info(ip)
            city_code = str(city_location['city_code'])

            if city_code in location_info.keys():
                location_info[city_code]['visit_num'] += 1
            else:    
                location_info[city_code] = {
                'longitude':float(city_location['longitude']) + random.random()*3.0 - 1.5,
                'latitude':float(city_location['latitude']) + random.random()*2.0 - 1.0,
                'visit_num': 1,
                }

            # 获取操作系统信息
            os_name = get_os_name(access_record.agent)
            os_info[os_name] = 1 if os_name not in os_info.keys() else os_info[os_name] + 1

            # 获取浏览器信息
            browser_name = get_browser_name(access_record.agent)
            browser_info[browser_name] = 1 if browser_name not in browser_info.keys() else browser_info[browser_name] + 1

            # 获取每日访问信息
            date = access_record.time.strftime('%Y-%m-%d %H:%M%S').split(' ')[0]
            day_visit_info[date] = 1 if date not in day_visit_info.keys() else day_visit_info[date] + 1

            # 总访问量
            total_visit_num += 1
        except ProcessNginxLogError, error:
            pass

    return {
    'location_info': location_info,
    'os_info': os_info,
    'browser_info': browser_info,
    'url_path_info': url_path_info,
    'day_visit_info': day_visit_info,
    'total_visit_num': total_visit_num,
    }

if __name__ == '__main__':
    test_process_nginx_access_log()
