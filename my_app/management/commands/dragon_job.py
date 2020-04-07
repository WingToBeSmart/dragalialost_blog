
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from datetime import datetime
from my_app.models import Dragon, Skill, Ability
from django.core.management.base import BaseCommand
from django.utils import timezone

BASE_URL = 'https://dragalialost.gamepedia.com{}'


class Command(BaseCommand):
    help = 'Import Dragons'

    def handle(self, *args, **kwargs):
        response = requests.get(BASE_URL.format('/Dragon_List'))
        soup = BeautifulSoup(response.text, features='html.parser')

        dragon_table = soup.find('table', class_='wikitable sortable')

        for row in dragon_table.find_all('tr')[1:]:
            dragon_dict = {}
            dragon_dict['availability'] = row.attrs.get(
                'data-availability')
            dragon_dict['group'] = row.attrs.get(
                'data-group')
            cells = row.find_all('td')
            for idx, item in enumerate(cells):
                if(idx == 0):
                    dragon_dict['name'] = cells[idx].find('a').get('title')
                    dragon_dict['icon_url'] = cells[idx].find(
                        'img').get('src')
                    dragon_dict['url'] = BASE_URL.format(
                        cells[idx].find('a').get('href'))
                elif(idx == 2):
                    dragon_dict['rarity'] = cells[idx].get_text(strip=True)
                elif(idx == 3):
                    dragon_dict['element'] = cells[idx].get_text(
                        strip=True)
                elif(idx == 4):
                    dragon_dict['hp'] = cells[idx].get_text(strip=True)
                elif(idx == 5):
                    dragon_dict['Str'] = cells[idx].get_text(strip=True)
                elif(idx == 6):
                    level_dict = {}
                    for i, value in enumerate(cells[idx].find('div', class_='tooltiptext').text.split(']')):
                        if(value != " "):
                            level_dict[f'level_{i+1}'] = f'{value}]'
                    skill = Skill(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'), **level_dict)
                    dragon_dict['skill'] = skill.save()
                elif(idx == 7):
                    image_list = []
                    name_list = []
                    for span_tag in cells[idx].find_all('span'):
                        if(span_tag.find('img')):
                            image_list.append(span_tag.find('img').get('src'))
                        if(span_tag.find('a')):
                            name_list.append(span_tag.find('a').get('title'))
                    ability_dict = {
                        'level': ['Lv. 1', 'Lv. 2'],
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
                elif(idx == 8):
                    image_list = []
                    name_list = []
                    for span_tag in cells[idx].find_all('span'):
                        if(span_tag.find('img')):
                            image_list.append(span_tag.find('img').get('src'))
                        if(span_tag.find('a')):
                            name_list.append(span_tag.find('a').get('title'))
                    ability_dict = {
                        'level': ['Lv. 1', 'Lv. 2'],
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
                elif(idx == 9):
                    dragon_dict['release_date'] = datetime.strptime(
                        cells[idx].get_text(strip=True), "%b %d, %Y").strftime('%Y-%m-%d')
                else:
                    pass

            dra = Dragon(**dragon_dict)
            dra = dra.save()
            for ab in ability_list:
                dra.ability_1.add(ab)
            for ab in ability_list_2:
                dra.ability_2.add(ab)
            if(dra.save()):
                self.stdout.write(self.style.SUCCESS(
                    'New Dragon is added: %s' % dra))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'New Dragon is existed: %s' % dra))

        self.stdout.write(self.style.SUCCESS(
            'End of process!'))
