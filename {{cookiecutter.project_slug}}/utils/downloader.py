import requests
from selenium import webdriver
from requests_file import FileAdapter

DOWNLOAD_SESSION = requests.Session()
DOWNLOAD_SESSION.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
DOWNLOAD_SESSION.mount('file://', FileAdapter())

def read(path, loadjs=False):
    try:
        if loadjs:
            driver = webdriver.PhantomJS()
            driver.get(path)
            time.sleep(5)
            return driver.page_source
        else:
            response = DOWNLOAD_SESSION.get(path, stream=True)
            response.raise_for_status()
            return response.content
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
        # If path is a local file path, try to open the file (generate hash if none provided)
        with open(path, 'rb') as fobj:
            return fobj.read()


