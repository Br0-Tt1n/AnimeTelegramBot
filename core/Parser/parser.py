import re
import mysql.connector as con

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class DarkLibriaSpider(scrapy.Spider):
    name = 'DarkLibria'
    start_urls = ['https://darklibria.it/releases/?&page=1']

    # Подключение базы данных к парсеру
    def __init__(self, *args, **kwargs):
        super(DarkLibriaSpider, self).__init__(*args, **kwargs)
        self.con = con.connect(
            host='localhost',
            user='_Br0_',
            password='kolokolikolokolpop009',
            database='test_database_for_1vBOT'
        )
        self.cursor = self.con.cursor()

    def parse(self, response):
        for h5 in response.css('td[class="torrent text-center h5"]'):
            anime_name = h5.css('a::attr(onclick)').get()
            description_name = re.search(r'"[^"]*"(,\s*"([^"]*)")', anime_name).group(2)
            anime_link = h5.css('a::attr(href)').get()

            self.insert_into_bd(anime_name=description_name, anime_link=anime_link)

            yield {
                'anime_link': anime_link,
                'anime_name': description_name
            }
        next_page = response.css('li[class="page-item  bg-dark"]:nth-last-of-type(2) a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        self.logger.info(f"Парсинг страницы: {response.url}")

    def insert_into_bd(self, anime_name, anime_link):
        try:
            self.cursor.execute("""
                INSERT INTO anime (anime_name, anime_link)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE anime_link = VALUES(anime_link);
            """, (anime_name, anime_link))
            self.con.commit()
        except con.Error as e:
            self.logger.error(f"Ошибка при вставке в базу данных: {e}")

    def close(self, reason):
        self.cursor.close()
        self.con.close()


process = CrawlerProcess(get_project_settings())
process.crawl(DarkLibriaSpider)
process.start()
