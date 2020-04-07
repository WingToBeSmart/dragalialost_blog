
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from datetime import datetime
from my_app.models import WeaponAbility, Weapon, Skill
from django.core.management.base import BaseCommand

BASE_URL = 'https://dragalialost.gamepedia.com{}'


class Command(BaseCommand):
    help = 'Import Weapon'

    def handle(self, *args, **kwargs):
        response = requests.get(BASE_URL.format('/Weapon_List'))
        soup = BeautifulSoup(response.text, features='html.parser')

        weapon_table = soup.find('table', class_='wikitable sortable center')

        for row in weapon_table.find_all('tr')[1:]:
            weapon_dict = {}
            weapon_dict['availability'] = row.attrs.get(
                'data-availability')
            weapon_dict['group'] = row.attrs.get(
                'data-weapon-group')
            cells = row.find_all('td')
            for idx, item in enumerate(cells):
                if(idx == 0):
                    weapon_dict['name'] = cells[idx].find('a').get('title')
                    weapon_dict['icon_url'] = cells[idx].find(
                        'img').get('src')
                    weapon_dict['url'] = BASE_URL.format(
                        cells[idx].find('a').get('href'))
                elif(idx == 2):
                    weapon_dict['rarity'] = cells[idx].get_text(strip=True)
                elif(idx == 3):
                    weapon_dict['weapon_type'] = cells[idx].get_text(
                        strip=True)
                elif(idx == 4):
                    weapon_dict['element'] = cells[idx].get_text(strip=True)
                elif(idx == 5):
                    weapon_dict['hp'] = cells[idx].get_text(strip=True)
                elif(idx == 6):
                    weapon_dict['Str'] = cells[idx].get_text(strip=True)
                elif(idx == 7):
                    if(cells[idx].find('a')):
                        level_dict = {}
                        for i, value in enumerate(cells[idx].text.split(']')):
                            if(len(value) != 0):
                                level_dict[f'level_{i+1}'] = f'{value}]'
                        skill = Skill(name=cells[idx].find('a').get(
                            'title'), icon_url=cells[idx].find('img').get('src'), **level_dict)
                        weapon_dict['skill'] = skill.save()
                elif(idx == 8):
                    if(cells[idx].find('a')):
                        ability = WeaponAbility(name=cells[idx].find('a').get(
                            'title'), icon_url=cells[idx].find('img').get('src'))
                        weapon_dict['ability_1'] = ability.save()
                elif(idx == 9):
                    if(cells[idx].find('a')):
                        ability = WeaponAbility(name=cells[idx].find('a').get(
                            'title'), icon_url=cells[idx].find('img').get('src'))
                        weapon_dict['ability_2'] = ability.save()
                elif(idx == 10):
                    weapon_dict['release_date'] = datetime.strptime(
                        cells[idx].get_text(strip=True), "%b %d, %Y").strftime('%Y-%m-%d')
                else:
                    pass

            wea = Weapon(**weapon_dict)
            if(wea.save()):
                self.stdout.write(self.style.SUCCESS(
                    'New Weapon is added: %s' % wea))
            else:
                self.stdout.write(self.style.SUCCESS(
                    'New Weapon is existed: %s' % wea))

        self.stdout.write(self.style.SUCCESS(
            'End of process!'))
