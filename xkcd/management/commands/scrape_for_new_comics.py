import logging
import os
import re
import requests

from boto3 import session
from boto3.s3.transfer import S3Transfer
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from local_settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_SPACES_URL, TEMP_IMAGE_DIRECTORY
from xkcd.models import Comic


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -  %(message)s')

AWS_SPACES_BUCKET = 'comic'


class Command(BaseCommand):
    def handle(self, *args, **options):
        comics = []
        counter = 0
        stored_comics = Comic.objects.all().order_by('-published')
        latest_number = stored_comics[0].number if stored_comics else 0

        # Get the xkcd homepage
        base_link = 'https://xkcd.com/'
        res = requests.get(base_link)
        res.raise_for_status()

        # Get the starting comic number
        page_soup = BeautifulSoup(res.text, features="html.parser")
        comic_number = re.search(r'(?<=https://xkcd.com/)\d+', page_soup.text).group(0)

        client = session.Session().client('s3', region_name='sfo2', endpoint_url=AWS_SPACES_URL,
                                          aws_access_key_id=AWS_ACCESS_KEY,
                                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        transfer = S3Transfer(client)

        while str(latest_number) != comic_number and counter < 20:
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
                logging.info(f'Downloading {basename}')

                # Save the image to disk
                filepath = os.path.join(TEMP_IMAGE_DIRECTORY, basename)
                img_file = open(filepath, 'wb')
                for chunk in img_res.iter_content(100000):
                    img_file.write(chunk)
                img_file.close()

                # Upload to spaces
                transfer.upload_file(filepath, 'comic', f'xkcd/{basename}')
                client.put_object_acl(ACL='public-read', Bucket=AWS_SPACES_BUCKET, Key=f'xkcd/{basename}')

                # Delete the temp image file saved to disk
                os.remove(filepath)

            except requests.exceptions.HTTPError:
                logging.info(f'Could not find xkcd {comic_number}')
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
                archive_link_number = int(link_list[i].get('href').replace('/', ''))

                if comics[i].number == archive_link_number:
                    comics[i].published = link_list[i].get('title')
                else:
                    logging.error(f"""Abort: comic ids do not line up with archive links.
                        downloaded comic: {comics[i].number}
                        archive page link: {archive_link_number}
                        Downloaded comics have not been recorded in the database.""")
                    return

            logging.info('Saving downloaded comics')
            Comic.objects.bulk_create(comics)

        logging.info('Comics are up to date.')
