import scrapy
from scrapy import Request

from movies.items import MoviesItem


class MoviesSpider(scrapy.Spider):
    name = "movies"

    def __init__(self):
        self.start_urls = [
            'https://www.rottentomatoes.com/celebrity/arnoldschwarzenegger',
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=False)

    def parse(self, response):
        items = []
        item = None

        for movie in response.xpath("//tbody[@class='celebrity-filmography__tbody']"):
            item = MoviesItem()
            item['title'] = movie.xpath('.//tr/td[2]/a/text()').extract()
            item['year'] = movie.xpath('.//tr/td[5]/text()').extract()
            rating = movie.xpath('.//tr/td/span/text()').extract()

            if (rating == "No Score Yet"):
                item['rating'] = rating
            else:
                item['rating'] = movie.xpath('.//tr/td/span/span[2]/text()').extract()

            items.append(item)

        #yield items
        for item in items:
            yield {
                "title": item['title'],
                "year": item['year'],
                "rating": item['rating']
            }
