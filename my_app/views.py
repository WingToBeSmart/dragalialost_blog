import requests
import pandas as pd
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from selenium import webdriver
# Create your views here.

BASE_URL = 'https://dragalialost.gamepedia.com{}'
NEWS_URL = 'https://dragalialost.com{}'


def home(request):
    news_response_lists = []
    showcase_response_lists = []
    new_adventurers_response_lists = []
    new_dragons_response_lists = []
    new_wyrmprints_response_lists = []
    response = requests.get(BASE_URL.format('/Dragalia_Lost_Wiki'))
    soup = BeautifulSoup(response.text, features='html.parser')

    void_battles_table = soup.find_all('table', class_='wikitable center')[0]
    void_battles_table_body = []
    void_battles_table_head = [
        th.text for th in void_battles_table.find_all('th')]
    for row in void_battles_table.find_all('tr'):
        void_battles_table_body.append(
            [cell.get_text(strip=True) for cell in row.find_all('td')])

    high_dragon_master_table = soup.find_all(
        'table', class_='wikitable center')[1]
    high_dragon_master_body = []
    high_dragon_master_head = [
        th.text for th in high_dragon_master_table.find_all('th')]
    for row in high_dragon_master_table.find_all('tr'):
        high_dragon_master_body.append(
            [cell.get_text(strip=True) for cell in row.find_all('td')])

    # for render news
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # driver = webdriver.Chrome(chrome_options=options)
    # driver.get(NEWS_URL.format('/cht'))
    # html = driver.execute_script("return document.documentElement.outerHTML")
    # sel_soup = BeautifulSoup(html, features='html.parser')

    # new_list = sel_soup.find_all('ul', class_='news-list')
    # for ul_tag in new_list:
    #     for li_tag in ul_tag.find_all('li'):
    #         new_list_url = NEWS_URL.format(li_tag.find('a').get('href'))
    #         if "http" in li_tag.find('img').get('src'):
    #             new_list_image = li_tag.find('img').get('src')
    #         else:
    #             new_list_image = NEWS_URL.format(li_tag.find('img').get('src'))
    #         new_list_title = li_tag.find(
    #             'p', class_='title').get_text(strip=True)
    #         new_list_time = li_tag.find(
    #             'div', class_='time').get_text(strip=True)[0:16]
    #         new_list_cat = li_tag.find('span').get_text(strip=True)
    #         news_response_lists.append(
    #             (new_list_image, new_list_url, new_list_title, new_list_time, new_list_cat))

    # for render showcase
    showcase_lists = soup.find_all('div', class_="SummonShowcaseMP")
    for showcase_list in showcase_lists:
        showcase_url = showcase_list.find_all('a')[1:2][0].get('href')
        showcase_title = showcase_list.find_all('a')[1:2][0].get('title')
        showcase_image = showcase_list.find('img').get('src')
        showcase_response_lists.append(
            (showcase_image, BASE_URL.format(showcase_url), showcase_title))

    # for render new adventurers
    adventurer_listings = soup.find_all('div', attrs={
        'style': 'width:100%;margin:5px;text-align:center;border:1px solid #9aa99a;'})[1:2]

    for adventurer_listing in adventurer_listings:
        for item in adventurer_listing.find_all('div', class_="tooltip"):
            adventurer_image = item.find('img').get('src')
            adventurer_url = item.find('a').get('href')
            adventurer_name = item.find('a').get('title')
            new_adventurers_response_lists.append(
                (adventurer_image, BASE_URL.format(adventurer_url), adventurer_name))

    # for render new dragons
    dragon_listings = soup.find_all('div', attrs={
        'style': 'width:100%;margin:5px;text-align:center;border:1px solid #9aa99a;'})[2:3]

    for dragon_listing in dragon_listings:
        for item in dragon_listing.find_all('div', class_="tooltip"):
            dragon_image = item.find('img').get('src')
            dragon_url = item.find('a').get('href')
            dragon_name = item.find('a').get('title')
            new_dragons_response_lists.append(
                (dragon_image, BASE_URL.format(dragon_url), dragon_name))

    # for render new wyrmprints
    wyrmprint_listings = soup.find_all('div', attrs={
        'style': 'width:100%;margin:5px;text-align:center;border:1px solid #9aa99a;'})[3:4]

    for wyrmprint_listing in wyrmprint_listings:
        for item in wyrmprint_listing.find_all('div', class_="tooltip"):
            wyrmprint_image = item.find('img').get('src')
            wyrmprint_url = item.find('a').get('href')
            wyrmprint_name = item.find('a').get('title')
            new_wyrmprints_response_lists.append(
                (wyrmprint_image, BASE_URL.format(wyrmprint_url), wyrmprint_name))

    # render all list to frontend
    stuff_for_frontend = {
        'news_response_lists': news_response_lists,
        'showcase_response_lists': showcase_response_lists,
        'new_adventurers_response_lists': new_adventurers_response_lists,
        'new_dragons_response_lists': new_dragons_response_lists,
        'new_wyrmprints_response_lists': new_wyrmprints_response_lists,
        'void_battles_table_head': void_battles_table_head,
        'void_battles_table_body': void_battles_table_body,
        'high_dragon_master_head': high_dragon_master_head,
        'high_dragon_master_body': high_dragon_master_body,

    }
    return render(request, 'index.html', stuff_for_frontend)


def adventurer(request):
    response = requests.get(BASE_URL.format('/Adventurer_List'))
    soup = BeautifulSoup(response.text, features='html.parser')

    adventurer_table = soup.find('table', class_='wikitable sortable')
    adventurer_table_body = []
    adventurer_table_head = []

    adventurer_table_head = adventurer_table.find_all('th')
    for idx, item in enumerate(adventurer_table_head):
        if(idx == 6 or idx == 7):
            if("HP" in adventurer_table_head[idx].find('div', class_="tooltip").text.upper()):
                name = "HP"
            else:
                name = "STR"
            adventurer_table_head[idx] = {
                'name': name,
                'description': adventurer_table_head[idx].find('div', class_="tooltiptext").text,
            }
        else:
            adventurer_table_head[idx] = adventurer_table_head[idx].get_text(
                strip=True)

    for row in adventurer_table.find_all('tr'):
        cells = row.find_all('td')
        for idx, item in enumerate(cells):
            if(idx == 0):
                cells[idx] = {
                    'name': cells[idx].find('a').get('title'),
                    'image': cells[idx].find('img').get('src'),
                    'url': BASE_URL.format(cells[idx].find('a').get('href')),
                }
            elif(idx == 5):
                cells[idx] = cells[idx].find('img').get('src')
            elif(idx == 8 or idx == 9):
                cells[idx] = {
                    'skill_name': cells[idx].find('a').get('title'),
                    'skill_image': cells[idx].find('img').get('src'),
                    'skill_url': BASE_URL.format(cells[idx].find('a').get('href')),
                    'skill_description': cells[idx].find('div', class_='tooltiptext').text.split(']')[0:-1],
                }
            else:
                cells[idx] = cells[idx].get_text(strip=True)

        adventurer_table_body.append(cells)

    # render data to frontend
    stuff_for_frontend = {
        'adventurer_table_head': adventurer_table_head,
        'adventurer_table_body': adventurer_table_body,
    }

    return render(request, 'adventurer.html', stuff_for_frontend)


def dragon(request):
    response = requests.get(BASE_URL.format('/Dragon_List'))
    soup = BeautifulSoup(response.text, features='html.parser')

    dragon_table = soup.find('table', class_='wikitable sortable')
    dragon_table_body = []
    dragon_table_head = [cells.get_text(strip=True)
                         for cells in dragon_table.find_all('th')]

    for row in dragon_table.find_all('tr'):
        cells = row.find_all('td')
        for idx, item in enumerate(cells):
            if(idx == 0):
                cells[idx] = {
                    'name': cells[idx].find('a').get('title'),
                    'image': cells[idx].find('img').get('src'),
                    'url': BASE_URL.format(cells[idx].find('a').get('href')),
                }
            elif(idx == 6):
                cells[idx] = {
                    'skill_name': cells[idx].find('a').get('title'),
                    'skill_image': cells[idx].find('img').get('src'),
                    'skill_url': BASE_URL.format(cells[idx].find('a').get('href')),
                    'skill_description': cells[idx].find('div', class_='tooltiptext').text.split(']')[0:-1],
                }
            elif(idx == 7 or idx == 8):
                image_list = []
                name_list = []
                url_list = []
                for span_tag in cells[idx].find_all('span'):
                    if(span_tag.find('img')):
                        image_list.append(span_tag.find('img').get('src'))
                    if(span_tag.find('a')):
                        name_list.append(span_tag.find('a').get('title'))
                        url_list.append(BASE_URL.format(
                            span_tag.find('a').get('href')))

                cells[idx] = {
                    'ability_level': ['Lv. 1', 'Lv. 2'],
                    'ability_name': name_list,
                    'ability_image': image_list,
                    'ability_url': url_list,
                    'ability_description': [i.text for i in cells[idx].find_all('div', class_="tooltiptext")],
                }
            else:
                cells[idx] = cells[idx].get_text(strip=True)

        dragon_table_body.append(cells)

    # render data to frontend
    stuff_for_frontend = {
        'dragon_table_head': dragon_table_head,
        'dragon_table_body': dragon_table_body,
    }

    return render(request, 'dragon.html', stuff_for_frontend)


def wyrmprint(request):
    response = requests.get(BASE_URL.format('/Wyrmprint_List'))
    soup = BeautifulSoup(response.text, features='html.parser')

    wyrumprint_table = soup.find('table', class_='wikitable sortable')
    wyrumprint_table_body = []
    wyrumprint_table_head = [cells.get_text(strip=True)
                             for cells in wyrumprint_table.find_all('th')]

    for row in wyrumprint_table.find_all('tr'):
        cells = row.find_all('td')
        for idx, item in enumerate(cells):
            if(idx == 0):
                cells[idx] = {
                    'name': cells[idx].find('a').get('title'),
                    'image': cells[idx].find('img').get('src'),
                    'url': BASE_URL.format(cells[idx].find('a').get('href')),
                }
            elif(idx == 5 or idx == 6 or idx == 7):
                image_list = []
                name_list = []
                url_list = []
                for span_tag in cells[idx].find_all('span'):
                    if(span_tag.find('img')):
                        image_list.append(span_tag.find('img').get('src'))
                    if(span_tag.find('a')):
                        name_list.append(span_tag.find('a').get('title'))
                        url_list.append(BASE_URL.format(
                            span_tag.find('a').get('href')))

                cells[idx] = {
                    'ability_level': ['Lv. 1', 'Lv. 2', 'Lv. 3'],
                    'ability_name': name_list,
                    'ability_image': image_list,
                    'ability_url': url_list,
                    'ability_description': [i.text for i in cells[idx].find_all('div', class_="tooltiptext")],
                }
            else:
                cells[idx] = cells[idx].get_text(strip=True)

        wyrumprint_table_body.append(cells)

    # render data to frontend
    stuff_for_frontend = {
        'wyrumprint_table_head': wyrumprint_table_head,
        'wyrumprint_table_body': wyrumprint_table_body,
    }

    return render(request, 'wyrmprint.html', stuff_for_frontend)
