import scrapy
import csv
import os
from scrapy.crawler import CrawlerProcess
from datetime import date


def update_csv(log, temp):
    with open(temp, 'r') as read_temp:
        temp_reader = csv.reader(read_temp, delimiter=',')
        next(temp_reader)
        for new_item in temp_reader:
            update = True

            with open(log, 'r') as read_log:
                log_reader = csv.reader(read_log, delimiter=',')
                for current_item in log_reader:
                    if new_item[1] == current_item[1]:
                        update = False

            if update:
                with open(log, 'a') as write_current:
                    csv.writer(write_current).writerow(new_item)

    os.remove(temp)


class FunSpider(scrapy.Spider):
    name = 'nonfungible'

    def start_requests(self):
        yield scrapy.Request(url='https://nonfungible.com/blog', callback=self.parse)

    def parse(self, response):
        categories = response.css('h5::text').extract()
        titles = response.css('h6>span::text').extract()
        contents = response.css('p>span::text').extract()
        with open(file=f'csv/temp.csv', mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=['category', 'title', 'content', 'date'])
            writer.writeheader()
            for i in range(3, len(titles)):
                writer.writerow({'category': categories[int(i/3)],
                                 'title': titles[i],
                                 'content': contents[i],
                                 'date': date.today()})


process = CrawlerProcess(settings={
})

if __name__ == '__main__':
    process.crawl(FunSpider)
    process.start()
    update_csv(f'csv/log.csv', f'csv/temp.csv')