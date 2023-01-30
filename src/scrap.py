import requests
from bs4 import BeautifulSoup

from src.utils import *


def extract_html(url):
    """
    Get html from url
    """

    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")

    return soup
