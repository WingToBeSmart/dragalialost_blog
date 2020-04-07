
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from datetime import datetime
from my_app.models import Wyrmprint, Ability
from django.core.management.base import BaseCommand

BASE_URL = 'https://dragalialost.gamepedia.com{}'


class Command(BaseCommand):
    help = 'Import Wyrmprint'

    def handle(self, *args, **kwargs):
        response = requests.get(BASE_URL.format('/Wyrmprint_List'))
        soup = BeautifulSoup(response.text, features='html.parser')

        wyrmprint_table = soup.find('table', class_='wikitable sortable')

        for row in wyrmprint_table.find_all('tr')[1:]:
            wyrmprint_dict = {}
            wyrmprint_dict['availability'] = row.attrs.get(
                'data-availability')
            cells = row.find_all('td')
            for idx, item in enumerate(cells):
                if(idx == 0):
                    wyrmprint_dict['name'] = cells[idx].find('a').get('title')
                    wyrmprint_dict['icon_url'] = cells[idx].find(
                        'img').get('src')
                    wyrmprint_dict['url'] = BASE_URL.format(
                        cells[idx].find('a').get('href'))
                elif(idx == 2):
                    wyrmprint_dict['rarity'] = cells[idx].get_text(strip=True)
                elif(idx == 3):
                    wyrmprint_dict['hp'] = cells[idx].get_text(strip=True)
                elif(idx == 4):
                    wyrmprint_dict['Str'] = cells[idx].get_text(strip=True)
                elif(idx == 5):
                    image_list = []
                    name_list = []
                    for span_tag in cells[idx].find_all('span'):
                        if(span_tag.find('img')):
                            image_list.append(span_tag.find('img').get('src'))
                        if(span_tag.find('a')):
                            name_list.append(span_tag.find('a').get('title'))
                    ability_dict = {
                        'level': ['Lv. 1', 'Lv. 2', 'Lv. 3'],
                        'name': name_list,
                        'icon_url': image_list,
                        'description': [i.text for i in cells[idx].find_all('div', class_="tooltiptext")],
                    }
                    ability_list = []
                    if len(ability_dict['name']) != 0:
                        for i in range(len(ability_dict['name'])):
                            ability = Ability(name=ability_dict['name'][i], level=ability_dict['level'][i],
                                              icon_url=ability_dict['icon_url'][i], description=ability_dict['description'][i])
                            ability_list.append(ability.save())
                elif(idx == 6):
                    image_list = []
                    name_list = []
                    for span_tag in cells[idx].find_all('span'):
                        if(span_tag.find('img')):
                            image_list.append(span_tag.find('img').get('src'))
                        if(span_tag.find('a')):
                            name_list.append(span_tag.find('a').get('title'))
                    ability_dict = {
                        'level': ['Lv. 1', 'Lv. 2', 'Lv. 3'],
                        'name': name_list,
                        'icon_url': image_list,
                        'description': [i.text for i in cells[idx].find_all('div', class_="tooltiptext")],
                    }
                    ability_list_2 = []
                    if len(ability_dict['name']) != 0:
                        for i in range(len(ability_dict['name'])):
                            ability = Ability(name=ability_dict['name'][i], level=ability_dict['level'][i],
                                              icon_url=ability_dict['icon_url'][i], description=ability_dict['description'][i])
                            ability_list_2.append(ability.save())
                elif(idx == 7):
                    image_list = []
                    name_list = []
                    for span_tag in cells[idx].find_all('span'):
                        if(span_tag.find('img')):
                            image_list.append(span_tag.find('img').get('src'))
                        if(span_tag.find('a')):
                            name_list.append(span_tag.find('a').get('title'))
                    ability_dict = {
                        'level': ['Lv. 1', 'Lv. 2', 'Lv. 3'],
                        'name': name_list,
                        'icon_url': image_list,
                        'description': [i.text for i in cells[idx].find_all('div', class_="tooltiptext")],
                    }
                    ability_list_3 = []
                    if len(ability_dict['name']) != 0:
                        for i in range(len(ability_dict['name'])):
                            ability = Ability(name=ability_dict['name'][i], level=ability_dict['level'][i],
                                              icon_url=ability_dict['icon_url'][i], description=ability_dict['description'][i])
                            ability_list_3.append(ability.save())
                elif(idx == 8):
                    wyrmprint_dict['release_date'] = datetime.strptime(
                        cells[idx].get_text(strip=True), "%b %d, %Y").strftime('%Y-%m-%d')
                else:
                    pass

            wyr = Wyrmprint(**wyrmprint_dict)
            wyr = wyr.save()
            for ab in ability_list:
                wyr.ability_1.add(ab)
            for ab in ability_list_2:
                wyr.ability_2.add(ab)
            for ab in ability_list_3:
                wyr.ability_3.add(ab)
            if(wyr.save()):
                self.stdout.write(self.style.SUCCESS(
                    'New Wyrmprint is added: %s' % wyr))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'New Wyrmprint is existed: %s' % wyr))

        self.stdout.write(self.style.SUCCESS(
            'End of process!'))
