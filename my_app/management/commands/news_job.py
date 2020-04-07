
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from selenium import webdriver
from datetime import datetime
from my_app.models import News
from django.core.management.base import BaseCommand

BASE_URL = 'https://dragalialost.com{}'


class Command(BaseCommand):
    help = 'Import News'

    def handle(self, *args, **kwargs):

        # for render news

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(BASE_URL.format('/cht'))
        html = driver.execute_script(
            "return document.documentElement.outerHTML")
        sel_soup = BeautifulSoup(html, features='html.parser')

        new_list = sel_soup.find_all('ul', class_='news-list')
        for ul_tag in new_list:
            for li_tag in ul_tag.find_all('li'):
                news_dict = {}
                news_dict['url'] = BASE_URL.format(
                    li_tag.find('a').get('href'))
                if "http" in li_tag.find('img').get('src'):
                    news_dict['image_url'] = li_tag.find('img').get('src')
                else:
                    news_dict['image_url'] = BASE_URL.format(
                        li_tag.find('img').get('src'))
                news_dict['name'] = li_tag.find(
                    'p', class_='title').get_text(strip=True)
                news_dict['release_date'] = datetime.strptime(
                    li_tag.find(
                        'div', class_='time').get_text(strip=True)[0:16], "%Y/%m/%d %H:%M")
                news_dict['category'] = li_tag.find(
                    'span').get_text(strip=True)
                news = News(**news_dict)
                if(news.save()):
                    self.stdout.write(self.style.SUCCESS(
                        'News is added: %s' % news))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        'News is existed: %s' % news))

        self.stdout.write(self.style.SUCCESS(
            'End of process!'))
