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
def visit_statistics(request):
    """用户访问报表
    """
    # 线上数据
    access_info = mongo.mongo_engine.get_access_info()

    return render_to_response('visit_record.html', {
        'location_info': json.dumps(access_info['location_info']),
        'os_info': json.dumps(access_info['os_info']),
        'browser_info': json.dumps(access_info['browser_info']),
        'url_path_info': json.dumps(access_info['url_path_info']),
        'day_visit_info': json.dumps(access_info['day_visit_info']),
        'total_visit_num': access_info['total_visit_num'],
        } )
