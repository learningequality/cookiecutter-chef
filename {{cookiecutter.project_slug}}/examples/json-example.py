import csv
import logging
import json
import os
import sys
import zipfile

sys.path.append(os.getcwd())

from utils import data_writer, path_builder, downloader
from le_utils.constants import licenses
from bs4 import BeautifulSoup

""" Run Configurations"""

CHANNEL_NAME = "Open Stax"
CHANNEL_SOURCE_ID = "open-stax"
CHANNEL_DOMAIN = "openstax.org"
CHANNEL_LANGUAGE = "en"
PATH = path_builder.PathBuilder(channel_name=CHANNEL_NAME)

""" Additional Configurations """

BASE_URL = "https://openstax.org/api"
ZIPNAME = "{}.zip".format(CHANNEL_NAME)
WRITE_TO_PATH = "{}{}{}.zip".format(os.path.dirname(os.path.realpath(__file__)), os.path.sep, CHANNEL_NAME)

# Map for Open Stax licenses to le_utils license constants
LICENSE_MAPPING = {
    "Creative Commons Attribution License": licenses.CC_BY,
    "Creative Commons Attribution-NonCommercial-ShareAlike License": licenses.CC_BY_NC_SA,
}
COPYRIGHT_HOLDER = "Rice University"
PDF_TITLE = "{} ({} Resolution)"
LOGGER = logging.getLogger()
__logging_handler = logging.StreamHandler()
LOGGER.addHandler(__logging_handler)
LOGGER.setLevel(logging.INFO)


""" Helper Methods """

def read_source(endpoint="books"):
    page_contents = downloader.read("{baseurl}/{endpoint}".format(baseurl=BASE_URL, endpoint=endpoint))
    return json.loads(page_contents) # Open Stax url returns json object

def parse_description(description):
    return BeautifulSoup(description or "", "html5lib").text

def generate_metadata(data):
    auth_data = {
        "license": LICENSE_MAPPING[data.get('license_name')],
        "license_description": data.get('license_text'),
        "copyright_holder": COPYRIGHT_HOLDER,
    }
    content_details = {
        "description": parse_description(data.get('description')),
        "thumbnail": writer.add_file(str(PATH), "thumbnail.png", data.get('cover_url'), write_data=False),
        "author": ", ".join([a.get('value').get('name') for a in data.get('authors')]),
    }
    content_details.update(auth_data)

    return auth_data, content_details

def scrape_source(writer):
    LOGGER.info("Parsing HTML from {}...".format(BASE_URL))

    contents = read_source() # Get json data from page

    for book in contents.get('books')[:1]:
        PATH.set(book.get('subject'), book.get('title')) # Topic hierarchy: Subject -> Title

        content = read_source(endpoint=book.get('slug'))

        if not content:
            continue    # Skip to next item

        auth_info, details = generate_metadata(content)

        writer.add_folder(str(PATH), book.get('title'), **details) # Write topic details

        # Read PDFs
        LOGGER.info("   Writing {} documents...".format(book.get('title')))
        writer.add_file(str(PATH), PDF_TITLE.format(content['title'], "High"), content.get("high_resolution_pdf_url"), **details)
        writer.add_file(str(PATH), PDF_TITLE.format(content['title'], "Low"), content.get("low_resolution_pdf_url"), **details)
        writer.add_file(str(PATH), "Student Handbook", content.get("student_handbook_url"), **details)

        # Parse resource materials
        LOGGER.info("   Writing {} resources...".format(book.get('title')))
        parse_resources("Instructor Resources", content.get('book_faculty_resources'), writer, **auth_info)
        parse_resources("Student Resources", content.get('book_student_resources'), writer, **auth_info)


def parse_resources(resource_name, resource_data, writer, **auth_info):
    resource_data = resource_data or []
    PATH.push(resource_name)
    writer.add_folder(str(PATH), resource_name)
    for resource in resource_data:
        if resource.get('link_document_url'):
            _name, ext = os.path.splitext(resource['link_document_url'])
            if ext.lower() == ".pdf":
                title = resource.get('resource_heading')
                description = parse_description(resource.get('resource_description'))
                LOGGER.info("      Writing resource {}...".format(title))
                writer.add_file(str(PATH), title, resource.get("link_document_url"), description=description, **auth_info)

    PATH.pop() # Go back one step in path


""" This code will run when the sushi chef is called from the command line. """
if __name__ == '__main__':

    # Open a writer to generate files
    with data_writer.DataWriter(write_to_path=WRITE_TO_PATH) as writer:

        # Write channel details to spreadsheet
        writer.add_channel(CHANNEL_NAME, CHANNEL_SOURCE_ID, CHANNEL_DOMAIN, CHANNEL_LANGUAGE)

        # Scrape source content
        scrape_source(writer)

        LOGGER.info("\n\nDONE: Zip created at {}\n".format(writer.write_to_path))


