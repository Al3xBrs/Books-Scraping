import requests
import shutil

from src.utils import *


def write_data_csv(data, f):
    """
    Write Data in the .csv file
    """

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


def save_img(img_url, data):
    """
    Save .png file in the assets 
    """
    res = requests.get(img_url, stream=True)

    img_name = f"{data['title']}.png".replace("/", "-").replace(';', '-')
    if res.ok:
        with open(DEST_ASSETS + img_name, "wb") as f:
            shutil.copyfileobj(res.raw, f)
