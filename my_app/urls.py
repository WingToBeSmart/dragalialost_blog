from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adventurer', views.adventurer, name='adventurer'),
    path('dragon', views.dragon, name='dragon'),
    path('wyrmprint', views.wyrmprint, name='wyrmprint'),
    path('weapon', views.weapon, name='weapon'),
    path('blog', views.blog, name='blog'),
]
