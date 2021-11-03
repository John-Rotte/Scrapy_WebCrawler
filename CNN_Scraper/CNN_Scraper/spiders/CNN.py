import scrapy
from CNN_Scraper.items import Article
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CnnSpider(CrawlSpider):
    name = 'CNN'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/2021/10/31/asia/china-japan-south-korea-covid-intl-dst-hnk/index.html']

    # If not working try r'\/2021\/[0-9][0-9]\/[0-9][0-9]\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'

    rules = [Rule(LinkExtractor(allow=r'\/2021\/[0-9][0-9]\/[0-9][0-9]\/[a-zA-Z\-]+\/[a-zA-Z\-]+\/index.html'),
             callback='parse', follow=True)]

    def parse(self, response):
        article = Article()
        article['url'] = response.url
        article['lastUpdated'] = response.xpath("//p[@class='update-time']/text()").get()
        article['title'] = response.xpath("//h1/text()").get()
        article['text'] = response.xpath("//div[@class='zn-body__paragraph']//text()").getall()
        return article
