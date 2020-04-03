
import schedule
import requests
import time
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from selenium import webdriver
from datetime import datetime

BASE_URL = 'https://dragalialost.gamepedia.com{}'
COUNT = 0


def do_job():
    response = requests.get(BASE_URL.format('/Adventurer_List'))
    soup = BeautifulSoup(response.text, features='html.parser')

    adventurer_table = soup.find('table', class_='wikitable sortable')
    adventurer_table_body = []
    adventurer_table_head = []

    for row in adventurer_table.find_all('tr')[1:2]:
        cells = row.find_all('td')
        adventurer_dict = {}
        for idx, item in enumerate(cells):
            if(idx == 0):
                adventurer_dict['name'] = cells[idx].find('a').get('title')
                adventurer_dict['icon'] = cells[idx].find('img').get('src')
                adventurer_dict['url'] = BASE_URL.format(
                    cells[idx].find('a').get('href'))
            elif(idx == 2):
                adventurer_dict['rarity'] = cells[idx].get_text(strip=True)
            elif(idx == 3):
                adventurer_dict['element'] = cells[idx].get_text(strip=True)
            elif(idx == 4):
                adventurer_dict['weapon'] = cells[idx].get_text(strip=True)
            elif(idx == 5):
                class_name = cells[idx].find('img').get('alt').upper()
                if("ATTACK" in class_name):
                    adventurer_dict['classname'] = "ATTACK"
                elif("DEFENSE" in class_name):
                    adventurer_dict['classname'] = "DEFENSE"
                elif("SUPPORT" in class_name):
                    adventurer_dict['classname'] = "SUPPORT"
                elif("HEALING" in class_name):
                    adventurer_dict['classname'] = "HEALING"
            elif(idx == 6):
                adventurer_dict['hp'] = cells[idx].get_text(strip=True)
            elif(idx == 7):
                adventurer_dict['Str'] = cells[idx].get_text(strip=True)
            elif(idx == 8):
                adventurer_dict['skill_1'] = {
                    'name': cells[idx].find('a').get('title'),
                    'icon': cells[idx].find('img').get('src'),
                }
                for i, value in enumerate(cells[idx].find('div', class_='tooltiptext').text.split(']')):
                    if(value != " "):
                        adventurer_dict['skill_1'][f'level_{i+1}'] = f'{value}]'
            elif(idx == 9):
                adventurer_dict['skill_2'] = {
                    'name': cells[idx].find('a').get('title'),
                    'icon': cells[idx].find('img').get('src'),
                }
                for i, value in enumerate(cells[idx].find('div', class_='tooltiptext').text.split(']')):
                    if(value != " "):
                        adventurer_dict['skill_2'][f'level_{i+1}'] = f'{value}]'
            elif(idx == 10):
                adventurer_dict['release_date'] = datetime.strptime(
                    cells[idx].get_text(strip=True), "%b %d, %Y").strftime('%Y-%m-%d')
            else:
                pass

        adventurer_table_body.append(adventurer_dict)

    print(adventurer_table_body[0])
    # adv = Adventurer(**adventurer_table_body[0])
    # adv.save()
    # print(adv)


schedule.every(5).seconds.do(do_job)

while True:
    schedule.run_pending()
    time.sleep(1)
