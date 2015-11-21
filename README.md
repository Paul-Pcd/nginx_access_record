# nginx_access_record
通过fluentd采集nginx日志，生成用户访问记录报表  

## 介绍
* fluentd采集nginx日志, 存入mongDB中
* Django处理mongDB中数据, 利用EChart展示用户访问记录报表

## 需求分析
用户访问记录报表包含如下信息:
* 根据访问ip生成全国热力图
  * 解析ip插入新集合ip: ip、城市名、经度、纬度、数量
* 根据path生成热门文章列表
  * 解析path插入新集合url_path: name, frequency
* 根据agent生成浏览器、OS等信息饼图
  * 解析agent插入新集合 browser: name, frequency
  * 解析agent插入新集合 os: name, frequency  
* 生成每天访问量曲线 
  * 每次访问插入新集合 day_visit: datetime, frequency
* 生成总的访问数量

## 详情
### nginx日志地址
/usr/local/var/log/nginx/access.log

### nginx日志格式
```
127.0.0.1 - - [20/Nov/2015:16:11:26 +0800] "GET /blog/index.php?r=articleFront/view&id=34 HTTP/1.1" 200 9435 "http://localhost:8008/blog/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0"
```
### mongoDB数据库信息
* 地址: 127.0.0.1:12345
* 数据库名: access_record
* 集合名 
  * nginx_access_record: 访问记录
  * ip: ip、城市编号、城市名、经度、纬度、访问数量
  * os: name、访问数量
  * browser：name、访问数量
  * url_path：name、访问数量
  * day_visit：data、访问数量

### mongoDB数据格式
```
{
    "_id":"564ec99e83fceca951000006",
    "host":"127.0.0.1",
    "user":"-",
    "method":"GET",
    "path":"/",
    "code":"200",
    "size":"90422",
    "referer":"-",
    "agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
    "time":"2015-11-20T07:19:52Z"
}
```
## 实现
理想情况是做成流式计算, 实时处理每条nginx日志, 然后对数据库进行增量更新.  
架构分为三层：  
* Fluentd处理每条nginx access日志, 并更新到相应的数据库集合中
* Django直接拿各集合的数据, 处理完之后传递给前端
* 前端依赖EChart进行展现
