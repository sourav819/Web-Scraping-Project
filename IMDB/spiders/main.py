import scrapy
from scrapy import Request

class projIMDB(scrapy.Spider):
    name='imdb'
    #start_urls=['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',callback=self.parse,headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    def parse(self,response):
        print('\n\n\n\n---------------')
        for i in response.css('.lister-item-header a'):
            movieName = i.css('::text').get()
            movieUrl = i.css('::attr(href)').get()
            
            dic = {
                'title' : movieName,
                'movieUrl' : movieUrl
            }
            yield response.follow(movieUrl, callback=self.parseInfo, meta=dic,headers={
               'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' 
            })

            nextPage = response.xpath('(//a[@class="lister-page-next next-page"]/@href)[2]').get()
            if nextPage:
               yield response.follow(nextPage,callback=self.parse,headers={
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
               }) 
            

    def parseInfo(self, response):
        
        #print(response.meta['movie'])
        duration = response.xpath('normalize-space((//li[@class="ipc-inline-list__item"])[3]/text())').get()
        genre = response.xpath('//a[@class="GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt"]/span/text()').getall()
        year = response.xpath('(//span[@class="TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"])[1]/text()').get()
        rating = response.xpath('(//span[@class="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"])[1]/text()').get()
        # print(duration)
        # print(genre)
        # print(year)
        # print(rating)
        # print(response.url)
       
        # print('---------------')
        yield {
            'title' : response.meta['title'],
            'duration' : duration,
            'genre' : genre,
            'year' : year,
            'rating' : rating
        }

        