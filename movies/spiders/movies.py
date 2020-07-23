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
        for movie in response.xpath('//div/div[@class="scroll-x"]/table/tbody[@class="celebrity-filmography__tbody"]/tr[@data-year]'):
            # item = MoviesItem()
            # items.append(item)
            title = movie.xpath('./td[2]/a/text()').get()
            year = movie.xpath('./td[5]/text()').get()

            # if (str(movie.xpath('./td/span[@data-rating]/text()').extract()[0]).contains("\n")):
            #     rating = "No ranking"
            # else:
            rating = movie.xpath('./td/span[@data-rating]/text()').extract_first()[0].strip()

            if (rating == ""):
                rating = movie.xpath('./td/span[@data-rating]/span[@class="icon__tomatometer-score"]/text()').extract_first()
            # if(len(rating) > 5):
            #    rating = "No Score Yet"

            yield {
                "title": title,
                "year": year,
                "rating": rating
            }

