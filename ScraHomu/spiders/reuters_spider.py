
from datetime import timedelta, datetime, date

import scrapy


class ReutersSpider(scrapy.Spider):
    name = "reuters"
    
    def start_requests(self):
        urls = [
            'http://www.reuters.com/resources/archive/us/20170401.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_index)

    def parse_index(self, response):
        date_str = response.url.split("/")[-1]
        date_str = date_str.split(".")[0]
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        # filename = '%s-%s.html' % (self.name, date_str)
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        self.log('Index page date=%s' % date_obj)
        
        headlines = response.css("div.module")[0].css("div.headlineMed")
        self.log('Find headlines = %d' % len(headlines))
        
        for news in headlines[0:5]:
            news_title = news.css("a::text").extract_first()
            news_url = news.css("a::attr(href)").extract_first()
            self.log("title: %s" % news_title)
            self.log("url: %s" % news_url)
            
            if "BRIEF" in news_title:
                continue
            if "UPDATE" in news_title:
                continue
            
            # yield { "title": news_title, "url": news_url, }
            yield scrapy.Request(url=news_url, callback=self.parse_news)
    
    
    
    def parse_news(self, response):
        title = response.css("h1.article-headline::text").extract_first()
        article = response.css("#article-text")
        lines = article.css("p::text").extract()
        body = " ".join(lines)
        yield {"title": title, "body": body}
    
    
#


