#!/usr/bin/python
#_*_ coding: utf-8 _*_

import json
import datetime
import mongo.common
import mongo.models
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
def visit_record(request):
    """展示用户访问报表
    """
    ip_list = mongo.common.mock_ip_list()
    os_list = mongo.common.mock_os_list()
    browser_list = mongo.common.mock_browser_list()
    url_path_list = mongo.common.mock_url_path_list()
    day_visit_list = mongo.common.mock_day_visit_list()
    total_visit_num = mongo.common.mock_total_visit_num()

    return render_to_response('visit_record.html', {
        'ip_list': ip_list,
        'os_list': os_list,
        'browser_list': browser_list,
        'url_path_list': url_path_list,
        'day_visit_list': day_visit_list,
        'total_visit_num': total_visit_num,
        } )
