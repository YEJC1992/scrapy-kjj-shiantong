import scrapy
import shiantong.settings as settings
import math


class EshianSpider(scrapy.Spider):
    name = 'eshian'
    #allowed_domains = ['eshian.com']
    data = {
        "pageNo": settings.pageNo,
        "releaseTime": settings.releaseTime,
        "releaseTime1": settings.releaseTime1,
        "typeName": settings.typeName,
        "belowStandard": settings.belowStandard,
        "brand": settings.brand,
        "releaseTimeX": settings.releaseTimeX,
        "releaseTime1X": settings.releaseTime1X,
        "brandX": settings.brandX,
        "typeNameX": settings.typeNameX,
        "belowStandardX": settings.belowStandardX,
        "pTypeName": settings.pTypeName,
        "pTypeId": settings.pTypeId,
        "diquName": settings.diquName,
        "diquId": settings.diquId,
        "buhegeName": settings.buhegeName,
        "buhegeId": settings.buhegeId,
        "territories": settings.territories
    }

    start_urls = ['http://www.eshian.com/sat/foodsampling']

    # for post
    def start_requests(self):
        print("start scrapy...")
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url, formdata=self.data, callback=self.parse)

    def parse(self, response):
        presentPage = int(response.xpath('//em')[0].xpath('string(.)').extract()[0])
        totalRows = int(response.xpath('//em')[1].xpath('string(.)').extract()[0])
        allPage = int(math.ceil(totalRows/20))
        table = response.xpath('//table[@class="table table-data-show"]')[0]
        tbody = table.xpath('./tbody')[0]
        tr_list = tbody.xpath('./tr')
        print(str(len(tr_list)))
        for tr_ele in tr_list:
            item = {}
            item['产品/Product'] = tr_ele.xpath(
                './td')[0].xpath('string(.)').extract()[0]
            item['规格型号'] = tr_ele.xpath(
                './td')[1].xpath('string(.)').extract()[0]
            item['生产日期/通报编号/Reference'] = tr_ele.xpath(
                './td')[2].xpath('string(.)').extract()[0]
            item['生产企业/Subject'] = tr_ele.xpath(
                './td')[3].xpath('string(.)').extract()[0]
            item['不合格项（标准值）/Substance/Hazard'] = tr_ele.xpath('./td')[4].xpath('./table/tbody/tr/td')[0].xpath('string(.)').extract()[0]
            item['检验结果/Analytical Result'] = tr_ele.xpath('./td')[4].xpath('./table/tbody/tr/td')[1].xpath('string(.)').extract()[0]
            item['发布单位/Notification from']=tr_ele.xpath(
                './td')[5].xpath('string(.)').extract()[0]
            item['发布日期/Date of case']=tr_ele.xpath(
                './td')[6].xpath('string(.)').extract()[0]
            yield item
        if presentPage < allPage:
            self.data['pageNo'] = str(int(self.data['pageNo'])+1)
            yield scrapy.FormRequest(url=self.start_urls[0], formdata=self.data, callback=self.parse)
            