import re
import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from xkcd.models import Comic


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = requests.get('https://xkcd.com/archive/')
        res.raise_for_status()

        archive_soup = BeautifulSoup(res.text, features="html.parser")
        archives = archive_soup.find(id='middleContainer').find_all('a')

        stored_comics = Comic.objects.all().reverse()
        latest_stored = stored_comics[0] if stored_comics else None
        comics = []

        for comic in archives:
            filename_base = img_filename = None
            number = comic.get('href').replace('/', '')

            if latest_stored and latest_stored.number == comic.number:
                break

            for ext in ('png', 'jpg', 'gif'):
                if img_filename:
                    break
                
                try:
                    filename_base = comic.text.lower().replace(' ', '_')
                    img_link = f'https://imgs.xkcd.com/comics/{filename_base}.{ext}'
                    
                    img_res = requests.get(img_link)
                    img_res.raise_for_status()

                    img_filename = filename_base + '.' + ext
                    print(f'Found xkcd {number} at {img_filename}')

                except requests.exceptions.HTTPError:
                    pass

            if not filename_base:
                xkcd_page_link = f'https://xkcd.com/{number}/'
                xkcd_page_res = requests.get(xkcd_page_link)
                xkcd_page_res.raise_for_status()

                xkcd_page_soup = BeautifulSoup(xkcd_page_res.text, features='html.parser')
                xkcd_page_middle = xkcd_page_soup.find(id='middleContainer')

                try:
                    permalink_pattern = 'https://imgs.xkcd.com/comics/(.+)$'
                    img_filename = re.search(permalink_pattern, xkcd_page_middle.text).group(1)
                    print(f'Found xkcd {number} at a custom location: {img_filename}')

                except (requests.exceptions.HTTPError, AttributeError) as e:
                    print(f'xkcd {number} not found: {e}')
                    continue

            if img_filename:
                comics.append(Comic(
                    number = number,
                    published = comic.get('title'),
                    display_name = comic.text,
                    img_filename = img_filename,
                ))

        Comic.objects.bulk_create(comics)
