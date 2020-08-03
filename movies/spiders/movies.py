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
        for movie in response.xpath('//div/div[@class="scroll-x"]/table/tbody[@class="celebrity-filmography__tbody"]/tr[@data-year]'):
            # item = MoviesItem()
            # items.append(item)

            name = movie.xpath('./td[2]/a/text()').get()
            date = movie.xpath('./td[5]/text()').get()

            # if (str(movie.xpath('./td/span[@data-rating]/text()').extract()[0]).contains("\n")):
            #     rating = "No ranking"
            # else:
            likeability = movie.xpath('./td/span[@data-rating]/text()').extract_first()[0].strip()

            if (likeability == ""):
                likeability = movie.xpath('./td/span[@data-rating]/span[@class="icon__tomatometer-score"]/text()').extract_first()

            if (likeability == "N"):
                likeability = "No Score Yet"
            # if(len(rating) > 5):
            #    rating = "No Score Yet"

            item = MoviesItem(title = name, year = date, rating = likeability)

            items.append(item)

        # items.sort(key=items['rating'])
        # for i in range(0, len(items)):
        #     print("Running i loop")
        #     for j in range(0, len(items) - i - 1):
        #         print("Running j loop")
        #         if len(items[j]['rating']) <= 3 and len(items[j]['rating']) <= 3:
        #             if items[j]['rating'] > items[j + 1]['rating']:
        #                 items[j], items[j + 1] = items[j + 1], items[j]
        #
        # print('items' + items)
     #   items = items.sort(key=items['rating'])
        items.sort(key=lambda x: x['rating'])

        for x in items:
            yield x
            # yield {
            #     'title': title,
            #     'year': year,
            #     'rating': rating
            # }
