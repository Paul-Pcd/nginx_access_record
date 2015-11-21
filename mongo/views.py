#!/usr/bin/python
#_*_ coding: utf-8 _*_

import json
import datetime
import mongo.models
import mongo.mock_data
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
def visit_record(request):
    """展示用户访问报表
    """
    ip_list = mongo.mock_data.mock_ip_list()
    os_list = mongo.mock_data.mock_os_list()
    browser_list = mongo.mock_data.mock_browser_list()
    url_path_list = mongo.mock_data.mock_url_path_list()
    day_visit_list = mongo.mock_data.mock_day_visit_list()
    total_visit_num = mongo.mock_data.mock_total_visit_num()

    return render_to_response('visit_record.html', {
        'ip_list': json.dumps(ip_list),
        'os_list': json.dumps(os_list),
        'browser_list': json.dumps(browser_list),
        'url_path_list': json.dumps(url_path_list),
        # 'day_visit_list': json.dumps(day_visit_list),
        'day_visit_list': day_visit_list,
        'total_visit_num': total_visit_num,
        } )
