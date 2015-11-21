#!/usr/bin/python
# _*_ coding:utf-8 _*_

def mock_ip_list():
    """返回一组测试数据用于测试ip
    """
    return [
    {
    'city_name': u'日照',
    'longitude': 119.46,
    'latitude': 35.42,
    'visit_num': 10,
    },
    {
    'city_name': u'齐齐哈尔',
    'longitude': 123.97,
    'latitude': 47.33,
    'visit_num': 2,
    },
    {
    'city_name': u'厦门',
    'longitude': '118.1',
    'latitude': '24.46',
    'visit_num': 20,
    },
    ]

def mock_os_list():
    """返回一组数据用于测试os
    """
    return [
    {
    'name': 'Mac OS',
    'visit_num': 20,
    },
    {
    'name': 'Windows 10',
    'visit_num': 30,
    }
    ]

def mock_browser_list():
    """返回一组数据用于测试browser
    """
    return [
    {
    'name': 'firefox',
    'visit_num': 10,
    },
    {
    'name': 'safiri',
    'visit_num': 20,
    }
    ]

def mock_url_path_list():
    """返回一组数据用于测试url_path
    """
    return [
    {
    'name': '/index.php',
    'visit_num': 10,
    },
    {
    'name': '/index.php?r=aritcle',
    'visit_num': 20,
    }
    ]

def mock_day_visit_list():
    """返回一组数据用于测试day_visit
    """
    return [
    {
    'date': '2015-11-19',
    'visit_num': 10,
    },
    {
    'date': '2015-11-18',
    'visit_num': 20,
    }
    ]

def mock_total_visit_num():
    """返回一组数据用于测试total_visit_num
    """
    return 10000
