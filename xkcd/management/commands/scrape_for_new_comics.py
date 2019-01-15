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

        stored_comics = Comic.objects.all().order_by('-published')
        latest_number = stored_comics[0].number if stored_comics else 0

        base_link = 'https://xkcd.com/'
        res = requests.get(base_link)

        # Get the comic number
        page_soup = BeautifulSoup(res.text, features="html.parser")
        comic_number = re.search(r'(?<=https://xkcd.com/)\d+', page_soup.text).group(0)

        while str(latest_number) != comic_number and counter < 5:
            res = requests.get(f'{base_link}/{comic_number}')
            res.raise_for_status()

            # Parse the page and find the comic image element
            page_soup = BeautifulSoup(res.text, features="html.parser")
            img_elem = page_soup.find(id='comic').img
            basename = os.path.basename(img_elem.get('src'))

            # Save the comic image to the disk
            try:
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
                comic_number -= 1
                continue

            # Save the comic data to the array to be persisted
            comics.append(Comic(
                number = int(comic_number),
                img_filename = basename,
                display_name = img_elem.get('alt'),
                description = img_elem.get('title'),
            ))

            # Find the link to the next comic page
            prev_link = page_soup.select('a[rel="prev"]')[0]
            comic_number = prev_link.get('href').replace('/', '')
            counter += 1

        # Find the published date for each downloaded comic on the archives page
        if comics:
            res = requests.get(f'{base_link}/archive')
            res.raise_for_status()

            # Parse the page and find the comic image element
            page_soup = BeautifulSoup(res.text, features="html.parser")
            link_list = page_soup.find(id='middleContainer').find_all('a', limit=len(comics))

            # Save the date from the archive link to the comic object
            for i in range(len(comics)):
                comics[i].published = link_list[i].get('title')

            print('Saving downloaded comics')
            Comic.objects.bulk_create(comics)

        print('Comics are up to date.')
