# coding: utf-8

import os
import urllib
import scrapy

class FllSpider(scrapy.Spider):
    name = 'fllspider'
    start_urls = ['http://blogs.oulipo.net/fll/sommaire/']
    # start_urls = ['file://' + os.path.dirname(os.path.abspath(__file__)) + '/blogs.oulipo.net/fll/sommaire/index.html']

    def parse(self, response):
        files = []

        # entretien
        for url in response.css('li#all-posts a::attr("href")').extract():
            files.append('./scrapped/' + self.getFilename(url))
            yield scrapy.Request(response.urljoin(url), self.parse_content)

        # complément d'enquête
        for url in ["http://blogs.oulipo.net/fll/complement-denquete/voyage-a-seesen/", "http://blogs.oulipo.net/fll/complement-denquete/entretien-avec-maroussia-naitchenko/"]:
            files.append('./scrapped/' + self.getFilename(url))
            yield scrapy.Request(response.urljoin(url), self.parse_content)

        flist = open('./pages.txt', 'w')
        data = '\n'.join(files)
        flist.write(data)

    def parse_content(self, response):
        title =  response.css('div#content div.hfeed h2').extract()[0]
        content =  response.css('div#content div.hfeed div.entry-content').extract()[0]
        commentsEls = response.css('div#content div.hfeed div.comments').extract()
        comments = ""
        if (len(commentsEls) > 0):
            comments = commentsEls[0]
        page = title + content + comments
        f = open('./scrapped/' + self.getFilename(response.url), 'w')
        f.write(page.encode('utf-8'))

    def getFilename(self, url):
        parts = url.decode('utf-8').split('/')
        name = parts[len(parts) - 2]
        return urllib.unquote(name).encode('ascii', errors='ignore') + ".html"

