
from datetime import timedelta, datetime, date

import scrapy


class ReutersSpider(scrapy.Spider):
    name = "reuters"

    def start_requests(self):
        urls = [
            'http://www.reuters.com/resources/archive/us/20170401.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date_str = response.url.split("/")[-1]
        date_str = date_str.split(".")[0]
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        # page = response.url.split("/")[-2]
        filename = '%s-%s.html' % (self.name, date_str)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Index page date=%s' % date_obj)

#


