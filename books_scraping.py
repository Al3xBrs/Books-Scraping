import requests
from bs4 import BeautifulSoup

product_url = 'https://books.toscrape.com/catalogue/set-me-free_988/index.html'

# Get data from one book
def extract_data(product_url):
    """
    Extract data from the book's url
    """

    response = requests.get(product_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'class' : 'table table-striped'})

    data = {}
    data['upc'] = table.find('td').text
    data['title'] = soup.find('div', {'class' : 'col-sm-6 product_main'}).find('h1').text
    data['price_including_tax'] = table.find('th', text = 'Price (incl. tax)').find_next_sibling('td').text.replace('Â','')
    data['price_excluding_tax'] = table.find('th', text = 'Price (excl. tax)').find_next_sibling('td').text.replace('Â','')
    data['number_available'] = table.find('th', text = 'Availability').find_next_sibling('td').text
    data['product_description'] = soup.find('div', {'id' : 'product_description'}).find_next_sibling('p').text.replace(',',';')

    #Get the category from the directory
    directory = []
    list_directory = soup.find('ul', {'class' : 'breadcrumb'}).findAll('li')
    for x in list_directory:
        directory.append(x)       
    #Take the 3th obj in the directory == category
    data['category'] = directory[2].text.strip()
    
    #Find star-rating class and take its score
    rating = soup.find('p', class_='star-rating')
    star_rating = rating['class'][1]
    data['review_rating'] = star_rating + ' Star(s)'

    img = soup.find('div', {'class' : 'item active'}).find('img')
    data['image_url'] = img['src'].replace('../../', 'https://books.toscrape.com/')

    return data

# Export data in a .csv file
def write_csv_file(data):
    column ='product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n'
    with open('books.csv', 'w') as f:
        f.write(column)
        f.write(product_url + ',' + data['upc'] + ',' + data['title']
        + ',' + data['price_including_tax'] + ',' + data['price_excluding_tax']
        + ',' + data['number_available'] + ',' + data['product_description']
        + ',' + data['category'] + ',' + data['review_rating'] 
        + ',' + data['image_url'])

    
if __name__ == '__main__':
    data = extract_data(product_url)
    write_csv_file(data)
    

