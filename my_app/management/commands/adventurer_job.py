
import requests
import time
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from selenium import webdriver
from datetime import datetime
from my_app.models import Adventurer, Skill, AdventurerAbility
from django.core.management.base import BaseCommand
from django.utils import timezone

BASE_URL = 'https://dragalialost.gamepedia.com{}'


class Command(BaseCommand):
    help = 'Import Adventurers'

    def handle(self, *args, **kwargs):
        response = requests.get(BASE_URL.format('/Adventurer_Detailed_List'))
        soup = BeautifulSoup(response.text, features='html.parser')

        adventurer_table = soup.find('table', class_='wikitable sortable')

        for row in adventurer_table.find_all('tr')[1:]:
            adventurer_dict = {}
            adventurer_dict['availability'] = row.attrs.get(
                'data-availability')
            cells = row.find_all('td')
            for idx, item in enumerate(cells):
                if(idx == 0):
                    adventurer_dict['name'] = cells[idx].find('a').get('title')
                    adventurer_dict['icon_url'] = cells[idx].find(
                        'img').get('src')
                    adventurer_dict['url'] = BASE_URL.format(
                        cells[idx].find('a').get('href'))
                elif(idx == 2):
                    adventurer_dict['title'] = cells[idx].get_text(strip=True)
                elif(idx == 3):
                    adventurer_dict['class_name'] = cells[idx].get_text(
                        strip=True).upper()
                elif(idx == 4):
                    adventurer_dict['rarity'] = cells[idx].get_text(strip=True)
                elif(idx == 5):
                    adventurer_dict['element'] = cells[idx].get_text(
                        strip=True)
                elif(idx == 6):
                    adventurer_dict['weapon'] = cells[idx].get_text(strip=True)
                elif(idx == 7):
                    adventurer_dict['hp'] = cells[idx].get_text(strip=True)
                elif(idx == 8):
                    adventurer_dict['Str'] = cells[idx].get_text(strip=True)
                elif(idx == 9):
                    level_dict = {}
                    for i, value in enumerate(cells[idx].find('div', class_='tooltiptext').text.split(']')):
                        if(value != " "):
                            level_dict[f'level_{i+1}'] = f'{value}]'
                    skill_1 = Skill(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'), **level_dict)
                    adventurer_dict['skill_1'] = skill_1.save()
                elif(idx == 10):
                    level_dict = {}
                    for i, value in enumerate(cells[idx].find('div', class_='tooltiptext').text.split(']')):
                        if(value != " "):
                            level_dict[f'level_{i+1}'] = f'{value}]'
                    skill_2 = Skill(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'), **level_dict)
                    adventurer_dict['skill_2'] = skill_2.save()
                elif(idx == 11):
                    co_ability = AdventurerAbility(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'))
                    adventurer_dict['co_ability'] = co_ability.save()
                elif(idx == 12):
                    chain_co_ability = AdventurerAbility(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'))
                    adventurer_dict['chain_co_ability'] = chain_co_ability.save()
                elif(idx == 13):
                    ability_1 = AdventurerAbility(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'))
                    adventurer_dict['ability_1'] = ability_1.save()
                elif(idx == 14):
                    ability_2 = AdventurerAbility(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'))
                    adventurer_dict['ability_2'] = ability_2.save()
                elif(idx == 15):
                    ability_3 = AdventurerAbility(name=cells[idx].find('a').get(
                        'title'), icon_url=cells[idx].find('img').get('src'))
                    adventurer_dict['ability_3'] = ability_3.save()
                elif(idx == 16):
                    adventurer_dict['defense'] = cells[idx].get_text(
                        strip=True)
                elif(idx == 17):
                    adventurer_dict['release_date'] = datetime.strptime(
                        cells[idx].get_text(strip=True), "%b %d, %Y").strftime('%Y-%m-%d')
                elif(idx == 18):
                    adventurer_dict['obtained_form'] = cells[idx].get_text(
                        strip=True)
                else:
                    pass

            adv = Adventurer(**adventurer_dict)
            if(adv.save()):
                self.stdout.write(self.style.SUCCESS(
                    'New Adventurer is added: %s' % adv))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'New Adventurer is existed: %s' % adv))

        self.stdout.write(self.style.SUCCESS(
            'End of process!'))
