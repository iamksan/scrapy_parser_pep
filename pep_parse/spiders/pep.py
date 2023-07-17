import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        peps = response.css('#numerical-index table.pep-zero-table tbody tr')
        for pep in peps.css('a::attr(href)'):
            yield response.follow(pep.get(), callback=self.parse_pep)

    def parse_pep(self, response):
        full_pep_name = response.css('.page-title::text').get().split()
        data = {
            'number': int(full_pep_name[1]),
            'name': ' '.join(full_pep_name[3:]),
            'status': response.css('abbr::text').get()
        }
        yield PepParseItem(data)
