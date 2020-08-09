import scrapy
from scrapy import Request

from movies.items import MoviesItem


class MoviesSpider(scrapy.Spider):
    name = "movies"

    def __init__(self):
        #search this URL
        self.start_urls = [
            'https://www.rottentomatoes.com/celebrity/arnoldschwarzenegger',
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=False)

    def parse(self, response):
        items = []
        for movie in response.xpath('//div/div[@class="scroll-x"]/table/tbody[@class="celebrity-filmography__tbody"]/tr[@data-year]'):

            #for every movie, get its name and date
            name = movie.xpath('./td[2]/a/text()').get()
            date = movie.xpath('./td[5]/text()').get()

            # get its rating
            likeability = movie.xpath('./td/span[@data-rating]/text()').extract_first()[0].strip()

            #if rating is a number, get the number rating
            if (likeability == ""):
                likeability = movie.xpath('./td/span[@data-rating]/span[@class="icon__tomatometer-score"]/text()').extract_first()
                likeability = likeability[0:likeability.index("%")]

            #if rating is not a %, set to No Score Yet
            if (likeability == "N"):
                likeability = "No Score Yet"
                rating = "No Score Yet"


            #make MoviesItem based on title, year, rating
            item = MoviesItem(title = name, year = date, rating = likeability)

            #add to movies list
            items.append(item)

        #sort by "number" with the No Score Yets at the end
        items.sort(key=lambda w: w['rating'])

        # store 100 ratings
        hundreds = []
        for mov in items:
            if mov['rating'] == "100":
                hundreds.append(mov)

        #remove all 100s (b/c they're strings, 100 is seen as less than 70, 80, etc b/c 1 < 7, so we
        #need to fix just 100s
        items = [mov for mov in items if mov['rating'] != '100']

        #find index of first No Score Yet
        for x in range(0, len(items)):
            if items[x]['rating'] == "No Score Yet":
                index = x
                break

        #add hundreds back in
        for x in hundreds:
            items.insert(index, x)

        #add percents to number ratings
        for x in range(0, index + len(hundreds)):
            items[x]['rating'] = items[x]['rating'] + "%"

        #put items in a json file
        for z in items:
            yield z
