import os
import re
import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from xkcd.models import Comic


class Command(BaseCommand):
    def handle(self, *args, **options):
        comics = []
        counter = 0

        stored_comics = Comic.objects.all().order_by('published')
        latest_number = stored_comics[0] if stored_comics else 0

        base_link = 'https://xkcd.com/'
        res = requests.get(base_link)
        next_number = ''

        while latest_number is not next_number and counter < 5:
            res = requests.get(f'{base_link}/{next_number}')
            res.raise_for_status()

            # Parse the page and find the comic image element
            page_soup = BeautifulSoup(res.text, features="html.parser")
            img_elem = page_soup.find(id='comic').img
            basename = os.path.basename(img_elem.get('src'))

            # Save the comic image to the disk
            try:
                img_res = requests.get(f'https://imgs.xkcd.com/comics/{basename}')
                img_res = requests.get(f'https://imgs.xkcd.com/comics/{basename}')
                img_res.raise_for_status()
                print(f'Downloading {basename}')

                # Save the image to ./xkcd. (from ATBS)
                filepath = os.path.join('xkcd_imgs', basename)
                img_file = open(filepath, 'wb')
                for chunk in img_res.iter_content(100000):
                    img_file.write(chunk)
                img_file.close()

            except requests.exceptions.HTTPError:
                print(f'Could not find xkcd {number}')
                next_number -= 1
                continue

            if not next_number:
                m = re.search(r'(?<=https://xkcd.com/)\d+', page_soup.text)
                next_number = m.group(0)

            # Save the comic data to the array to be persisted
            comics.append(Comic(
                number = int(next_number),
                img_filename = basename,
                display_name = img_elem.get('alt'),
                description = img_elem.get('title'),
            ))

            # Find the link to the next comic page
            prev_link = page_soup.select('a[rel="prev"]')[0]
            next_number = prev_link.get('href').replace('/', '')
            counter += 1

        print('Saving downloaded comics')
        Comic.objects.bulk_create(comics)
