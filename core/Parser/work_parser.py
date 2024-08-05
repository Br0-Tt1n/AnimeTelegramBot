import re
import mysql.connector as con

import scrapy
from scrapy.crawler import CrawlerProcess

from core.settings import settings_bd


class DarkLibriaSpider(scrapy.Spider):
    name = 'DarkLibria'
    start_urls = ['https://darklibria.it/releases/?&page=1']

    page_count = 0

    # Подключение базы данных к парсеру
    def __init__(self, *args, **kwargs):
        super(DarkLibriaSpider, self).__init__(*args, **kwargs)
        self.con = con.connect(
            host=settings_bd.datadb.host,
            user=settings_bd.datadb.user,
            port=int(settings_bd.datadb.port),
            password=settings_bd.datadb.password,
            database=settings_bd.datadb.database
        )
        self.cursor = self.con.cursor()

    def parse(self, response, **kwargs):
        for h5, episodes, status in zip(response.css('td[class="torrent text-center h5"]'),
                                        response.css(
                                            'table[class="table table-sm table-bordered table-sm table-dark"]'
                                        ),
                                        response.css('span[class^="badge container-fluid badge-"]')):
            anime_name = h5.css('a::attr(onclick)').get()
            description_name = re.search(r'"[^"]*"(,\s*"([^"]*)")', anime_name).group(2)

            anime_link = h5.css('a::attr(href)').get()

            anime_episodes = episodes.css('div[class="d-xs-block d-sm-none"] span::text').get()

            anime_status = status.css("::text").get()
            if anime_status == "В РАБОТЕ":
                bool_status = True
            else:
                bool_status = False

            anime_id = self.check_anime_in_table_anime(anime_name=description_name, anime_link=anime_link)
            if anime_id:
                # Вычленяем номер последней выпущенной серии из бд
                episodes_str = str(self.episodes_comparison(description_name, anime_link)[0])
                episodes_from_anime = re.findall(r'\d+', episodes_str)

                # Из парсера
                episodes_parser = re.findall(r'\d+', anime_episodes)

                if episodes_from_anime and episodes_parser:
                    episodes_from_anime = episodes_from_anime[-1]
                    episodes_parser = episodes_parser[-1]

                    try:
                        if int(episodes_from_anime) < int(episodes_parser):
                            self.update_episodes(description_name, anime_link, anime_episodes, bool_status)
                            yield {'anime': [anime_id[0], description_name, anime_link, episodes_parser]}
                    except (TypeError, Exception):
                        continue
            else:
                self.insert_into_bd(anime_name=description_name, anime_link=anime_link,
                                    anime_episodes=anime_episodes, status=bool_status)

        next_page = response.css('li[class="page-item  bg-dark"]:nth-last-of-type(2) a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.page_count += 1
            if self.page_count < 4:
                yield scrapy.Request(next_page, callback=self.parse)

        self.logger.info(f"Парсинг страницы: {response.url[-1]}")

    def insert_into_bd(self, anime_name, anime_link, anime_episodes, status):
        try:
            self.cursor.execute("""
                INSERT INTO anime (anime_name, anime_link, anime_episodes, status)
                VALUES (%s, %s, %s, %s);
            """, (anime_name, anime_link, anime_episodes, status))
            self.con.commit()
        except con.Error as e:
            self.logger.error(f"Ошибка при вставке в базу данных: {e}")

    def check_anime_in_table_anime(self, anime_name, anime_link):
        check_work_query = """
            SELECT id FROM anime
            WHERE anime_name = %s AND anime_link = %s 
        """
        self.cursor.execute(check_work_query, (anime_name, anime_link))
        result_user = self.cursor.fetchone()
        return result_user

    def episodes_comparison(self, anime_name, anime_link):
        check_episodes_query = """
            SELECT anime_episodes FROM anime
            WHERE anime_name = %s AND anime_link = %s 
        """
        self.cursor.execute(check_episodes_query, (anime_name, anime_link))
        result_user = self.cursor.fetchone()
        return result_user

    def update_episodes(self, anime_name, anime_link, episodes, status):
        try:
            update_episodes_query = """
                UPDATE anime
                SET anime_episodes = %s, status = %s
                WHERE anime_name = %s AND anime_link = %s; 
            """
            self.cursor.execute(update_episodes_query, (episodes, status, anime_name, anime_link))
            self.con.commit()
        except Exception as e:
            print(e)

    def close(self, reason):
        self.cursor.close()
        self.con.close()


process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'core/Parser/save_data/anime_new_series.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    })
process.crawl(DarkLibriaSpider)
process.start()
