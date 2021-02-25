# -*- coding: utf-8 -*-
import scrapy
import re

#gen command: scrapy genspider stocks baidu.com
#run command: scrapy crawl stocks

class StocksSpider(scrapy.Spider):
    name = "stocks"
    start_urls = ['http://quote.eastmoney.com/stock_list.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}", href)[0]
                url = 'https://xueqiu.com/S/'+str.upper(stock)
                yield scrapy.Request(url,callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        infoDict = {}
        name = response.css(' .stock-name').extract()[0]
        quote = response.css('.quote-info')
        keyList = quote.css('td').extract()
        valueList = quote.css('span').extract()

        for i in range(len(keyList)):
            key = re.findall(r'<td>(.*?)<span',keyList[i])[0]
            try:
                val = re.findall(r'>(.*?)</span>',valueList[i])[0]
            except:
                val = '--'
            infoDict[key] = val

        infoDict.update(
            {'Stock name':re.findall(r'<div.*?class="stock-name">(.*?)</div',name)[0].split()[0]})
        yield infoDict