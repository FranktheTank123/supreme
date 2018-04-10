# import scrapy
# import datetime

# SCRAP_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# class SupremeShopperSpider(scrapy.Spider):
#     name = "supreme_shopper"

#     def start_requests(self):
#         urls = [
#             'http://www.supremenewyork.com/shop/all'
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         date = response.css('h1::text').re('\d{4}-\d{2}-\d{2}')
#         for item in response.css('div.masonry__item'):
#             yield {
#                 'droplist date': date,
#                 'name': item.css('h5::text').extract(),
#                 'price': item.css('span::text').re('\$[0-9]+'),
#                 'upvote': item.css('div.progress-bar.progress-bar-success.droplist-vote-bar::text').extract(),
#                 'downvote': item.css('div.progress-bar.progress-bar-danger.droplist-vote-bar::text').extract(),
#                 'scrapy date': SCRAP_DATE
#             }

#         items = response.css('div.inner-article').css('a::attr(href)').extract()
#         for item in items:
#             if item.css('div.sold_out_tag::text').extract() is not None:
#                 item_page = items.css('a::attr(href)').extract()
#             item_page = response.urljoin(item_page)
#             yield scrapy.Request(item_page, callback=self.parse)

