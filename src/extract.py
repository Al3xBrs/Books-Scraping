from src.utils import *
from src.scrap import extract_html


def extract_url_categories(url):
    """
    Extract all categories url
    """

    list_categories = []
    soup = extract_html(url)
    categories_url = soup.find(
        "ul", class_="nav nav-list").find("ul").find_all("li")

    for li in categories_url:
        a = li.find("a")
        href = BASE_URL + \
            a["href"]

        list_categories.append(href)

    return list_categories


def extract_data_category(category_url):
    """
    Extract data from the category
    """

    category = {}
    soup = extract_html(category_url)
    category['name'] = soup.find('li', class_='active').text
    category['pages'] = extract_pages_category(category_url)

    return category


def extract_pages_category(category_url):
    """
        Extract all pages from the category
    """

    soup = extract_html(category_url)
    pages = soup.find("li", class_="current")
    if pages is not None:
        pages = pages.text.strip()
        y = pages[10]
        y = int(y) + 1
        list_pages = []

        for i in range(1, y):
            list_pages.append(category_url.replace(
                "index.html", "") + f"page-{i}.html")

        return list_pages

    else:
        list_pages = [category_url]

        return list_pages


def extract_products_urls(list_page):
    """
    Extract url products page from each category page
    """
    list_products_url = []
    for page in list_page:
        soup_page = extract_html(page)
        list_products_url.extend(extract_books_url(soup_page))

    return list_products_url


def extract_books_url(soup_page):
    """
    Get all the product_url from the full category
    """

    list_product_url = []
    h3 = soup_page.find("ol", class_="row").find_all("h3")

    for h in h3:
        a = h.find("a")
        href = a["href"].replace(
            "../../../", "https://books.toscrape.com/catalogue/")
        list_product_url.append(href)

    return list_product_url


def extract_data(product_url):
    """
    Extract data from the book's url
    """
    soup = extract_html(product_url)
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
        .text.replace("Â", "").replace("£", "")
    )
    data["price_excluding_tax"] = (
        table.find("th", text="Price (excl. tax)")
        .find_next_sibling("td")
        .text.replace("Â", "").replace("£", "")
    )

    number_available = (
        table.find("th", text="Availability").find_next_sibling(
            "td").text.replace("(", "")
    )
    number = number_available.split()
    data["number_available"] = number[2]

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
    if star_rating == "Zero":
        star_rating = 0
    if star_rating == "One":
        star_rating = 1
    if star_rating == "Two":
        star_rating = 2
    if star_rating == "Three":
        star_rating = 3
    if star_rating == "Four":
        star_rating = 4
    if star_rating == "Five":
        star_rating = 5

    data["review_rating"] = str(star_rating)

    img = soup.find("div", {"class": "item active"}).find("img")
    data["image_url"] = img["src"].replace(
        "../../", "https://books.toscrape.com/")

    return data
