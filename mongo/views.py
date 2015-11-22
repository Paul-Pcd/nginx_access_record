#!/usr/bin/python
#_*_ coding: utf-8 _*_

import json
import datetime
import mongo.models
import mongo.mock_data
import mongo.mongo_engine
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
def visit_record(request):
    """展示用户访问报表
    """
    # 测试用数据
    # ip_info = mongo.mock_data.mock_ip_info()
    # day_visit_info = mongo.mock_data.mock_day_visit_info()
    # os_info = mongo.mock_data.mock_os_info()
    # browser_info = mongo.mock_data.mock_browser_info()
    # url_path_info = mongo.mock_data.mock_url_path_info()
    # total_visit_num = mongo.mock_data.mock_total_visit_num()

    # 线上数据
    city_info = mongo.mongo_engine.get_city_info()
    day_visit_info = mongo.mongo_engine.get_day_visit_info()
    os_info = mongo.mongo_engine.get_os_info()
    browser_info = mongo.mongo_engine.get_browser_info()
    url_path_info = mongo.mongo_engine.get_url_path_info()
    total_visit_num = mongo.mongo_engine.get_total_visit_num()

    return render_to_response('visit_record.html', {
        'city_info': city_info,
        'os_info': os_info,
        'browser_info': browser_info,
        'url_path_info': url_path_info,
        'day_visit_info': day_visit_info,
        'total_visit_num': total_visit_num,
        } )
