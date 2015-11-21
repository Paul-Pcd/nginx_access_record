#!/usr/bin/python
# _*_ coding:utf-8 _*_

from django.test import TestCase
from mongo.models import *

# 连接至mongoDB, 选择access_record数据库
connect('access_record', host = '127.0.0.1', port=12345)

# Create your tests here.
class NginxAccessRecordTestCase(TestCase):
    """mongo.models.NginxAccessRecord单元测试
    """
    def test_get_nginx_access_record(self):
        """遍历NginxAccessRecord集合
        """
        assert NginxAccessRecord.objects.count() != 0

class IpTestCase(TestCase):
    """mongo.models.Ip单元测试
    ip = StringField()
    longitude = FloatField()
    latitude = FloatField()
    visit_num = IntField()
    city_code = IntField()
    privince = StringField()
    city = StringField()
    district = StringField()
    street = StringField()
    street_number = StringField()
    """
    def setUp(self):
        ip = Ip(
            ip='121.41.119.102',
            longitude = 40,
            latitude = 40,
            visit_num = 10,
            city_code = 34,
            privince = u'北京',
            city = u'北京',
            district = '',
            street = '',
            street_number = '',
            )

        try:
            ip.save()
        except NotUniqueError, error: 
            ip_set = Ip.objects(ip='121.41.119.102')

            ip = ip_set[0]
            ip.visit_num = ip.visit_num + 1
            ip.save()

    def test_get_ip(self):
        ip_set = Ip.objects(ip='121.41.119.102')
        assert ip_set.count() == 1
        ip = ip_set[0]
        assert ip.ip == '121.41.119.102'

class OsTestCase(TestCase):
    """mongo.models.Os单元测试
    """
    def setUp(self):
        os = Os(
            name = 'Mac OS',
            visit_num = 10,
            )

        try:
            os.save()
        except NotUniqueError, error:
            os_set = Os.objects(name='Mac OS')
            assert os_set.count() == 1
            os = os_set[0]
            os.visit_num = os.visit_num + 1
            os.save()

    def test_get_os(self):
        os_set = Os.objects(name='Mac OS')
        assert os_set.count() == 1

        os = os_set[0]
        assert os.name == 'Mac OS'

class BrowserTestCase(TestCase):
    """mongo.models.Browser单元测试
    """
    def setUp(self):
        browser = Browser(
            name = 'firefox',
            visit_num = 10,
            )

        try:
            browser.save()
        except NotUniqueError, error:
            browser_set = Browser.objects(name='firefox')
            assert browser_set.count() == 1

            browser = browser_set[0]
            browser.visit_num = browser.visit_num + 1
            browser.save()

    def test_get_Browser(self):
        browser_set = Browser.objects(name='firefox')
        assert browser_set.count() == 1

        browser = browser_set[0]
        assert browser.name == 'firefox'

class UrlPathTestCase(TestCase):
    """mongo.models.UrlPath单元测试
    """
    def setUp(self):
        url_path = UrlPath(
            name = '/index.php',
            visit_num = 10,
            )

        try:
            url_path.save()
        except NotUniqueError, error:
            url_path_set = UrlPath.objects(name='/index.php')
            assert url_path_set.count() == 1

            url_path = url_path_set[0]
            url_path.visit_num = url_path.visit_num + 1
            url_path.save()

    def test_get_url_path(self):
        url_path_set = UrlPath.objects(name='/index.php')
        assert url_path_set.count() == 1

        url_path = url_path_set[0]
        assert url_path.name == '/index.php'

class DayVisitTestCase(TestCase):
    """mongo.models.DayVisit单元测试
    """
    def setUp(self):
        day_visit = DayVisit(
            date = '2015-11-21',
            visit_num = 10,
            )

        try:
            day_visit.save()
        except NotUniqueError, error:
            day_visit = DayVisit.objects(date='2015-11-21')
            assert day_visit.count() == 1

            day_visit = day_visit[0]
            day_visit.visit_num = day_visit.visit_num + 1
            day_visit.save()

    def test_get_day_visit(self):
        day_visit_set = DayVisit.objects(date='2015-11-21')
        assert day_visit_set.count() == 1

        day_visit = day_visit_set[0]
        assert day_visit.date == '2015-11-21'
