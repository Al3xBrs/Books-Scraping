import requests, shutil, os

from bs4 import BeautifulSoup

from src.extract import *
from src.save import *
from src.scrap import *

from src.utils import *


def main(url, category_url):
    """ main"""

    soup = extract_html(url)

    list_categories = extract_category(soup)

    state = 1
    for category_url in list_categories:
        soup_category = extract_html(category_url)
        list_page = extract_pages_category(soup_category)

        category_name = (
            category_url.replace(category_url, "").replace("/index.html", "") + ".csv"
        )
        with open(DEST_DATA + category_name, "w") as f:
            column = "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n"
            f.write(column)

        for page in list_page:
            soup_page = extract_html(page)
            list_product_url = extract_books_url(soup_page)

            for product_url in list_product_url:
                soup_product = extract_html(product_url)
                data = extract_data(soup_product)
                save_img(data["image_url"])
                write_data_csv(data, f)

                print("State :" + str(state))
                state = state + 1

    print("Job done !")


if __name__ == "__main__":
    main(
        url=BASE_URL,
        category_url=CATEGORY_URL,
    )
