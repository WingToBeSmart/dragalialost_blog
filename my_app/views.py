import requests
import pandas as pd
from django.shortcuts import render
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from selenium import webdriver
from datetime import datetime
from .models import Adventurer, Skill, News, AdventurerAbility, Wyrmprint, Dragon, WeaponAbility, Weapon
# Create your views here.

BASE_URL = 'https://dragalialost.gamepedia.com{}'


def home(request):
    showcase_response_lists = []
    new_adventurers_response_lists = []
    new_dragons_response_lists = []
    new_wyrmprints_response_lists = []
    new_mana_spirals_response_lists = []
    response = requests.get(BASE_URL.format('/Dragalia_Lost_Wiki'))
    soup = BeautifulSoup(response.text, features='html.parser')

    void_battles_table = soup.find_all('table', class_='wikitable center')[0]
    void_battles_table_body = []
    void_battles_table_head = [
        th.text for th in void_battles_table.find_all('th')]
    for row in void_battles_table.find_all('tr')[1:]:
        void_battles_table_body.append(
            [cell.get_text(strip=True) for cell in row.find_all('td')])

    high_dragon_master_table = soup.find_all(
        'table', class_='wikitable center')[1]
    high_dragon_master_body = []
    high_dragon_master_head = [
        th.text for th in high_dragon_master_table.find_all('th')]
    for row in high_dragon_master_table.find_all('tr')[1:]:
        high_dragon_master_body.append(
            [cell.get_text(strip=True) for cell in row.find_all('td')])

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

    # for render new mana spirals
    mana_spirals_listings = soup.find_all('div', attrs={
        'style': 'width:100%;margin:5px;text-align:center;border:1px solid #9aa99a;'})[4:5]

    for mana_spirals_listing in mana_spirals_listings:
        for item in mana_spirals_listing.find_all('div', class_="tooltip"):
            mana_spirals_image = item.find('img').get('src')
            mana_spirals_url = item.find('a').get('href')
            mana_spirals_name = item.find('a').get('title')
            new_mana_spirals_response_lists.append(
                (mana_spirals_image, BASE_URL.format(mana_spirals_url), mana_spirals_name))

    # render all list to frontend
    stuff_for_frontend = {
        'news_response_lists': News.objects.all().values('id', 'url', 'image', 'name', 'release_date', 'category'),
        'showcase_response_lists': showcase_response_lists,
        'new_adventurers_response_lists': new_adventurers_response_lists,
        'new_dragons_response_lists': new_dragons_response_lists,
        'new_wyrmprints_response_lists': new_wyrmprints_response_lists,
        'new_mana_spirals_response_lists': new_mana_spirals_response_lists,
        'void_battles_table_head': void_battles_table_head,
        'void_battles_table_body': void_battles_table_body,
        'high_dragon_master_head': high_dragon_master_head,
        'high_dragon_master_body': high_dragon_master_body,

    }
    return render(request, 'index.html', stuff_for_frontend)


def adventurer(request):
    # adventurer = Adventurer.objects.all()
    adventurer = Adventurer.objects.order_by('-release_date')
    paginator = Paginator(adventurer, 10, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))
    # render data to frontend
    # print(adventurer[0].skill_1)
    stuff_for_frontend = {
        'adventurer_list': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator
    }

    return render(request, 'adventurer.html', stuff_for_frontend)


def dragon(request):
    dragon = Dragon.objects.order_by('-release_date')
    paginator = Paginator(dragon, 10, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))
    # render data to frontend

    stuff_for_frontend = {
        'dragon_list': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator
    }

    return render(request, 'dragon.html', stuff_for_frontend)


def wyrmprint(request):
    wyrmprint = Wyrmprint.objects.order_by('-release_date')
    paginator = Paginator(wyrmprint, 10, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))
    # render data to frontend

    stuff_for_frontend = {
        'wyrmprint_list': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator
    }
    return render(request, 'wyrmprint.html', stuff_for_frontend)


def weapon(request):
    weapon = Weapon.objects.order_by('-rarity')
    paginator = Paginator(weapon, 10, orphans=5)

    is_paginated = True if paginator.num_pages > 1 else False
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        raise Http404(str(e))
    # render data to frontend

    stuff_for_frontend = {
        'weapon_list': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator
    }

    return render(request, 'weapon.html', stuff_for_frontend)


def blog(request):
    return render(request, 'blog.html')
