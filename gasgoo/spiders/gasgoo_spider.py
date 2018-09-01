# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from gasgoo.items import GasgooItem
import scrapy,re


class GasgooSpiderSpider(scrapy.Spider):
    name = 'gasgoo_spider'
    # allowed_domains = ['i.gasgoo.com']
    start_urls = ['http://i.gasgoo.com/supplier/c-968/index-1.html']
    
    cookie = {
        'ASP.NET_SessionId': '40l32h450fc5yw55eqwvbg55',
        'safedog-flow-item': 'F1714EAA1C72B758DC365FFF78CA9063'
    }
    meta = {
        # 禁止网页重定向
        'dont_redirect': True, 
        # 对哪些异常返回进行处理
        'handle_httpstatus_list': [301, 302]  
    }
    # def start_requests(self):
    #     baseUrl1 = 'http://i.gasgoo.com/supplier/c-{type}.html'
    #     baseUrl2 = 'http://i.gasgoo.com/supplier/oemcategorysearch.aspx?cid={no}'
    #     # 类别2
    #     typeList = [
    #         '968','863','300','304','298','301','302','299','301',
    #         '302','299','742','833','834','835','836','837','838'
    #     ]
    #     # 类别1
    #     noList = list(range(1, 6))

    #     start_urlslist = []
    #     for type in typeList:
    #         start_urlslist.append(baseUrl1.format(type=type))
            
    #     for no in noList:
    #         start_urlslist.append(baseUrl2.format(no=no))

    #     for start_urls in start_urlslist:
    #         yield scrapy.Request(url=start_urls,callback=self.parse)
    
    def parse(self, response):
        urlList = response.xpath("//div[@class='companylist']//p//a/@href").extract()
        for url in urlList:
            if re.match(r'http://i.gasgoo.com/supplier/\d+',url,flags=0):
                # print("现在开始爬取：{}".format(url))
                yield scrapy.Request(url, callback=self.parseCompany1)
                continue
            else:
                yield scrapy.Request(url, callback=self.parseCompany2)
        
        # 实现翻页爬取
        nextUrl = response.xpath("//div[@id='rpSearchResultList']/a[@class='next']/@href").extract()[0]
        if len(nextUrl):
            pattern = re.compile('index-(.*?).html')
            print('======')
            print(pattern.findall(url))
            if (pattern.findall(url)==[]):
                referer = 'None'
            else:
                index = int(pattern.findall(url)[0])
                referer = 'http: // i.gasgoo.com/supplier/c-968/index-{}.html'.format(index-1)
            headers = {
                'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8',
                'Accept-Language': 'zh-CN, zh;q = 0.9',
                'Connection': 'keep-alive',
                'Referer': referer
            }
            print("这里是headers")
            print(headers)
            yield scrapy.Request(nextUrl, callback=self.parse,headers=headers)

    def parseCompany1(self,response):
        item = GasgooItem()
        # print('===================')
        # print(response.request.headers.getlist('Cookie'))
        item['name'] = response.xpath("//div[@class='comleftAA']/h2/text()").extract()[0]
        item['abstract'] = response.xpath("//div[@class='Companyprofile']//p[@id='description']/text()").extract()[0]
        item['product'] = response.xpath("//div[@class='Customer margintop']//p[@id='product']/text()").extract()[0]
        item['client'] = response.xpath("//div[@class='Customer margintop']//p[@id='maintypicClient']/text()").extract()[0]
        # 公司基本信息
        infos = response.xpath("//div[@class='COMinfofr margintop']//li").extract()
        mapDict1 = {'公司性质': 'property', '公司地区': 'region', '公司网址': 'companyUrl', 
                   '成立时间': 'time', '法人代表': 'corporation', '注册资金': 'fund', '质量体系': 'quality'}
    
        pattern1 = re.compile('<span>(.*?)</span>')
        pattern2 = re.compile('</span>(.*?)</li>')
        pattern3 = re.compile('<a href="#" rel="nofollow">(.*?)</a>')

        for info in infos:
            # 先清洗
            info = info.replace('\r', '').replace('\n', '').strip()
            k = ''.join(pattern1.findall(info))

            if k in mapDict1.keys():
                if k == '公司网址':
                    v = ''.join(pattern3.findall(info))
                    # print(v)
                else:
                    v = ''.join(pattern2.findall(info)).replace('\r', '').replace('\n', '').strip()
                item[mapDict1[k]] = v
            else:
                continue
        # 联系信息
        contacts = response.xpath("//ul[@class='context']/li").extract()
        print(contacts)
        mapDict2 = {'公司电话': 'tel', '地址': 'address', '公司邮编': 'post'}
        pattern1 = re.compile('<span>(.*?)</span>')
        pattern2 = re.compile('</span>(.*?)</li>')

        if contacts:
            for contact in contacts:
                contact = contact.replace('\r', '').replace('\n', '').strip()
                k = ''.join(pattern1.findall(contact))

                if k in mapDict2.keys():
                    v = ''.join(pattern2.findall(contact)).replace('\r', '').replace('\n', '').strip()
                    item[mapDict2[k]] = v
                    break
                
        yield item
    
    def parseCompany2(self,response):
        item = GasgooItem()
        item['name'] = response.xpath("//h1/text()").extract()[0].replace('\r', '').replace('\n', '').strip()
        item['abstract'] = response.xpath("//dl[@class='presentation']//div/text()").extract()[0].replace('\r', '').replace('\n', '').strip()
        item['info'] = response.xpath("//ul[@class='firmA']//li").extract()

        yield item
