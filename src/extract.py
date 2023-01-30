import requests
from bs4 import BeautifulSoup
import shutil
import os


from src.utils import *


def extract_category(soup):
    """
    Extract the categories from the page
    # Get the list of categories

    """

    list_categories = []
    category_urls = soup.find("ul", class_="nav nav-list").find("ul").find_all("li")
    for li in category_urls:
        a = li.find("a")
        href = a["href"].replace(
            "../", "https://books.toscrape.com/catalogue/category/books/"
        )
        list_categories.append(url + href)

    return list_categories


def extract_pages_category(soup):
    """
    # Get number of page from a category
        Extract all pages from the category
    """

    pages = soup.find("li", class_="current")
    if pages is not None:
        pages = pages.text.strip()
        y = pages[10]
        y = int(y) + 1
        list_page = []

        for i in range(1, y):
            list_page.append(category_url.replace("index.html", "") + f"page-{i}.html")

        return list_page

    else:
        list_page = [category_url]

        return list_page


def extract_books_url(soup):
    """
    # Get books url from all category pages
    Get all the product_url from the full category
    """

    list_url = []
    h3 = soup.find("ol", class_="row").find_all("h3")

    for h in h3:
        a = h.find("a")
        href = a["href"].replace("../../../", "https://books.toscrape.com/catalogue/")
        list_url.append(href)

    return list_url


# Get data from a book
def extract_data(soup):
    """
    Extract data from the book's url
    """

    table = soup.find("table", {"class": "table table-striped"})

    data = {}
    data["product_page_url"] = product_url
    data["upc"] = table.find("td").text
    data["title"] = (
        soup.find("div", {"class": "col-sm-6 product_main"})
        .find("h1")
        .text.replace(",", ";")
    )
    data["price_including_tax"] = (
        table.find("th", text="Price (incl. tax)")
        .find_next_sibling("td")
        .text.replace("Â", "")
    )
    data["price_excluding_tax"] = (
        table.find("th", text="Price (excl. tax)")
        .find_next_sibling("td")
        .text.replace("Â", "")
    )
    data["number_available"] = (
        table.find("th", text="Availability").find_next_sibling("td").text
    )

    description = soup.find("div", {"id": "product_description"})
    if description is not None:
        data["product_description"] = description.find_next_sibling("p").text.replace(
            ",", ";"
        )
    else:
        data["product_description"] = ""

    # Get the category from the directory
    directory = []
    list_directory = soup.find("ul", {"class": "breadcrumb"}).findAll("li")
    for x in list_directory:
        directory.append(x)
    # Take the 3th obj in the directory == category
    data["category"] = directory[2].text.strip()

    # Find star-rating class and take its score
    rating = soup.find("p", class_="star-rating")
    star_rating = rating["class"][1]
    data["review_rating"] = star_rating + " Star(s)"

    img = soup.find("div", {"class": "item active"}).find("img")
    data["image_url"] = img["src"].replace("../../", "https://books.toscrape.com/")

    return data
