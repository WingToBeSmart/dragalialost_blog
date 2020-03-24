import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
# Create your views here.

BASE_URL = 'https://dragalialost.gamepedia.com{}'


def home(request):
    news_response_lists = []
    showcase_response_lists = []
    new_adventurers_response_lists = []
    new_dragons_response_lists = []
    new_wyrmprints_response_lists = []
    response = requests.get(BASE_URL.format('/Dragalia_Lost_Wiki'))
    soup = BeautifulSoup(response.text, features='html.parser')

    new_listings = soup.find_all('div', class_="SecondaryEventsMP")
    for new_list in new_listings:
        new_listing_image = new_list.find('img').get('src')
        new_list_url = new_list.find_all('a')[0:1][0].get('href')
        new_list_title = new_list.find_all('a')[0:1][0].get('title')
        official_new_list_url = new_list.find_all('a')[2:3][0].get('href')
        news_response_lists.append(
            (new_listing_image, BASE_URL.format(new_list_url), new_list_title, official_new_list_url))

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
    }
    return render(request, 'index.html', stuff_for_frontend)
