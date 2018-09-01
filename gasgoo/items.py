# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GasgooItem(scrapy.Item):
    # 公司名称
    name = scrapy.Field()
    # 成立时间
    time = scrapy.Field()
    # 主营产品
    product = scrapy.Field()
    # 配套客户
    client = scrapy.Field()
    # 公司性质
    property = scrapy.Field()
    # 公司地区
    region = scrapy.Field()
    # 公司URL
    companyUrl = scrapy.Field()
    # 法人代表
    corporation = scrapy.Field()
    # 注册资金
    fund = scrapy.Field()
    # 质量体系
    quality = scrapy.Field()
    # 公司简介
    abstract = scrapy.Field()
    # 公司电话
    tel = scrapy.Field()
    # 公司邮编
    post = scrapy.Field()
    # 公司地址
    address = scrapy.Field()
    # 信息
    info = scrapy.Field()
    
