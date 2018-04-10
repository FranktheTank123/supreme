import scrapy
import datetime

SCRAP_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

class SupremeSpider(scrapy.Spider):
    name = "supreme"

    def start_requests(self):
        urls = [
            'https://www.supremecommunity.com/season/spring-summer2018/droplists/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date = response.css('h1::text').re('\d{4}-\d{2}-\d{2}')
        for item in response.css('div.masonry__item'):
            yield {
                'droplist date': date,
                'name': item.css('h5::text').extract(),
                'price': item.css('span::text').re('\$[0-9]+'),
                'upvote': item.css('div.progress-bar.progress-bar-success.droplist-vote-bar::text').extract(),
                'downvote': item.css('div.progress-bar.progress-bar-danger.droplist-vote-bar::text').extract(),
                'scrapy date': SCRAP_DATE
            }

        next_pages = response.css('div.col-sm-4.col-xs-12').xpath('a/@href').extract()
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            print next_page
            yield scrapy.Request(next_page, callback=self.parse)

