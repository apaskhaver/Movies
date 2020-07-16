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

        for movie in response.xpath("//tbody[@class='celebrity-filmography__tbody']"):
                item = MoviesItem()
                item.title = movie.xpath('.//tr[@data-title]').extract_first()
                item.year = movie.xpath('.//tr[@data-year]').extract_first()
                item.rating = movie.xpath('.//tr[@data-rating]').extract_first()
                items.append(item)
