import requests

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.generic.base import TemplateView


def xkcds(request):
    res = requests.get('https://xkcd.com/archive/')
    res.raise_for_status()

    archives = BeautifulSoup(res.text).find(id='middleContainer')
    xkcds = []

    for x in archives.find_all('a'):
        xkcd = x.get('href').replace('/', '')
        date = x.get('title')
        name = x.text
        link = name.lower().replace(' ', '_')
        
        item = { 'xkcd': xkcd, 'date': date, 'name': name, 'link': link }
        xkcds.append(item)
    
    return JsonResponse(xkcds[:100], safe=False)
