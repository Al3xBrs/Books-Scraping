import requests
from bs4 import BeautifulSoup
import shutil
import os


def write_data_csv(data, f):
    """# Write Data in the .csv file"""

    with open(category_name, "a") as f:
        f.write(
            data["product_page_url"]
            + ","
            + data["upc"]
            + ","
            + data["title"]
            + ","
            + data["price_including_tax"]
            + ","
            + data["price_excluding_tax"]
            + ","
            + data["number_available"]
            + ","
            + data["product_description"]
            + ","
            + data["category"]
            + ","
            + data["review_rating"]
            + ","
            + data["image_url"]
            + "\n"
        )


# Save img in the directory
def save_img(img_url):
    res = requests.get(img_url, stream=True)
    # img_name = data['title'] + '.png'.replace('/', '-')
    img_name = f"{data['title']}.png".replace("/", "-")
    if res.ok:
        with open(img_name, "wb") as f:
            shutil.copyfileobj(res.raw, f)
