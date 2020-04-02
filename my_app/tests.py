from django.test import TestCase
from django.test.client import Client
from bs4 import BeautifulSoup
from .models import Adventurer, Skill
import requests

try:
    basestring
except NameError:
    basestring = str


# class MyClient(Client):
#     def request(self, **request):
#         response = super(MyClient, self).request(**request)
#         try:
#             response.soup = BeautifulSoup(response.content, "html.parser")
#         except:
#             response.soup = None
#         return response


class AdventurerModelTests(TestCase):
    # client_class = MyClient

    def test_import_data_adventurer(self):
        response = requests.get(
            'https://dragalialost.gamepedia.com/Dragalia_Lost_Wiki')
        new_adventurer = Adventurer(name='hello')
        self.assertEqual(new_adventurer.name, 'faliks')
        self.assertEqual(response.status_code, 200)
