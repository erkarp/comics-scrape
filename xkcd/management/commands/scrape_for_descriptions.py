import re
import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from xkcd.models import Comic

class Command(BaseCommand):
    def handle(self, *args, **options):

        for comic in Comic.objects.all():
            if comic.description:
                break
            
            res = requests.get(f'https://xkcd.com/{comic.number}/')
            res.raise_for_status()
            xkcd_page_soup = BeautifulSoup(res.text, features="html.parser")

            img_tag = xkcd_page_soup.find('img', {'alt' : comic.display_name})
            comic.description = img_tag.get('title')
            comic.save()
            