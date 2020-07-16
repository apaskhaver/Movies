import scrapy
from scrapy import Request

from movies.items import MoviesItem


class MoviesSpider(scrapy.Spider):
    name = "movies"

    def __init__(self):
        self.start_urls = [
            'https://www.rottentomatoes.com/celebrity/arnoldschwarzenegger',
        ]

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=False)

    def parse(self, response):
        items = []

        for movie in response.xpath("//tbody[@class='celebrity-filmography__tbody']"):
            if (str(movie.xpath('./a/text()').extract_first()) != "\n"):
                item = MoviesItem()
                item.title = movie.xpath('.//tr[@data-title]').extract_first()
                item.year = movie.xpath('.//tr[@data-year]').extract_first()
                item.rating = movie.xpath('.//tr[@data-rating]').extract_first()
                items.append(item)

       # next_page_url = response.xpath("//ul[@class='pagination-list']/li[last()]/a/@href").extract_first()

        # if the next page is not empty
        # go to it
      #  yield scrapy.Request(response.urljoin(next_page_url))