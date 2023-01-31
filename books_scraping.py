from src.extract import *
from src.save import *
from src.utils import *


def main(url):
    """
    main
    """

    list_categories = extract_url_categories(url)
    for category_url in list_categories:
        data_category = extract_data_category(category_url)
        list_pages = extract_pages_category(category_url)
        list_products_url = extract_products_urls(list_pages)

        with open(DEST_DATA + data_category['name'] + '.csv', "w") as f:
            column = "product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n"
            f.write(column)
            for product_url in list_products_url:
                data = extract_data(product_url)
                save_img(data["image_url"], data)
                write_data_csv(data, f)


if __name__ == "__main__":
    main(
        url=BASE_URL,
    )
