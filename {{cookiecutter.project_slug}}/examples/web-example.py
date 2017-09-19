#!/usr/bin/env python

# Import modules that will be required for web-scraping.
###########################################################
import requests
import os
import sys
import logging

sys.path.append(os.path.dirname(os.getcwd()))

from bs4 import BeautifulSoup
from utils import data_writer, path_builder, downloader
from le_utils.constants import licenses


# Fill out the channel settings here.
###########################################################
CHANNEL_TITLE = 'Wikipedia'                # a humand-readbale title
CHANNEL_DESCRIPTION = ''                   # description of this channel
CHANNEL_DOMAIN = 'en.wikipedia.org'        # domain of this channel
CHANNEL_SOURCE_ID = 'wikipedia'            # an alphanumeric ID refering to this channel
CHANNEL_LANGUAGE = 'en'                    # language of channel
CHANNEL_LICENSE = licenses.PUBLIC_DOMAIN   # Licenses used in this channel
CHANNEL_THUMBNAIL = 'https://lh3.googleusercontent.com/' \
                    + 'zwwddqxgFlP14DlucvBV52RUMA-cV3vRvmjf' \
                    + '-iWqxuVhYVmB-l8XN9NDirb0687DSw=w300'# link to the channel's thumbnail


# Fill out the Sous Chef settings here. 
###########################################################
CHANNEL_CSV_FILENAME = 'Channel.csv'
CHANNEL_SETTINGS = ['Title', 'Description', 'Domain', 'Source ID', 'Language', 'License ID', 'Thumbnail']
CONTENT_CSV_FILENAME = 'Content.csv'
CONTENT_SETTINGS = ['Path', 'Title', 'Description', 'Author', 'Language', 'License ID', 'License Description', 'Copyright Holder', 'Thumbnail']
PATH = path_builder.PathBuilder(channel_name=CHANNEL_TITLE)
ZIP_PATH = "{}{}{}.zip".format(os.path.dirname(os.path.realpath(__file__)), os.path.sep, CHANNEL_TITLE)


# Logger settings
###########################################################
LOGGER = logging.getLogger()
__logging_handler = logging.StreamHandler()
LOGGER.addHandler(__logging_handler)
LOGGER.setLevel(logging.INFO)


# Helper functions for web-scraping
###########################################################
def make_fully_qualified_url(url):
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return "https://en.wikipedia.org" + url
    assert url.startswith("http"), "Bad URL (relative to unknown location): " + url
    return url


def get_parsed_html_from_url(url):
    html = downloader.read(url)
    return BeautifulSoup(html, 'html.parser')


def download_wikipedia_page(url, thumbnail, title):
    # Generate details of a single page
    details = {
        'thumbnail': thumbnail,
        'source_id': url.split("/")[-1],
        'license': CHANNEL_LICENSE,
    }

    return details


# Start scraping the website
###########################################################
def scrape_source(writer):
    PATH.set()
    LOGGER.info('Parsing HTML from {}...'.format('https://en.wikipedia.org/wiki'))

    PATH.push('Citrus!')
    LOGGER.info('   Writing {} resources...'.format('Citrus!'))
    citrus_details = add_subpages_from_wikipedia_list(writer, 'https://en.wikipedia.org/wiki/List_of_citrus_fruits')
    writer.add_folder(str(PATH), 'Citrus!', **citrus_details)
    PATH.pop()
    
    PATH.push('Potatoes!')
    LOGGER.info('   Writing {} resources...'.format('Potatoes!'))
    potatoes_details = add_subpages_from_wikipedia_list(writer, "https://en.wikipedia.org/wiki/List_of_potato_cultivars")
    writer.add_folder(str(PATH), 'Potatoes!', **potatoes_details)
    PATH.pop()


def add_subpages_from_wikipedia_list(writer, list_url):

    # to understand how the following parsing works, look at:
    #   1. the source of the page (e.g. https://en.wikipedia.org/wiki/List_of_citrus_fruits), or inspect in chrome dev tools
    #   2. the documentation for BeautifulSoup version 4: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

    # parse the the page into BeautifulSoup format, so we can loop through and manipulate it
    page = get_parsed_html_from_url(list_url)

    folder_details = {}

    # extract the main table from the page
    table = page.find("table")

    # loop through all the rows in the table
    for row in table.find_all("tr"):

        # extract the columns (cells, really) within the current row
        columns = row.find_all("td")

        # some rows are empty, so just skip
        if not columns:
            continue

        # get the link to the subpage
        link = columns[0].find("a")

        # some rows don't have links, so skip
        if not link:
            continue

        # extract the URL and title for the subpage
        url = make_fully_qualified_url(link["href"])
        title = link.text

        LOGGER.info("      Writing {} resources...".format(title))

        # attempt to extract a thumbnail for the subpage, from the second column in the table
        image = columns[1].find("img")
        thumbnail_url = make_fully_qualified_url(image["src"]) if image else None
        if thumbnail_url and not (thumbnail_url.endswith("jpg") or thumbnail_url.endswith("png")):
            thumbnail_url = None

        # download the wikipedia page and add file in the path
        details = download_wikipedia_page(url, thumbnail=thumbnail_url, title=title)
        writer.add_file(str(PATH), title, url, **details)

    return folder_details


# Main function to create the Sous Chef
###########################################################
if __name__ == '__main__':
    with data_writer.DataWriter(write_to_path=ZIP_PATH) as writer:
        writer.add_channel(CHANNEL_TITLE, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, 
            CHANNEL_LANGUAGE, CHANNEL_DESCRIPTION, CHANNEL_THUMBNAIL)
        scrape_source(writer)

        LOGGER.info("\n\nDONE: Zip created at {}\n".format(ZIP_PATH))
