import requests
from bs4 import BeautifulSoup
import shutil
import os

# Get html from url
def extract_html(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    
    return soup

# Get the list of categories
def extract_category(soup):
    """
    Extract the categories from the page
    """
    
    list_categories = []
    category_urls = soup.find('ul', class_='nav nav-list').find('ul').find_all('li')
    for li in category_urls:
        a = li.find('a')
        href = a['href'].replace('../', 'https://books.toscrape.com/catalogue/category/books/')
        list_categories.append(url + href)

    return list_categories

# Get number of page from a category
def extract_pages_category(soup):
    """
    Extract all pages from the category
    """

    pages = soup.find('li', class_='current')
    if pages is not None:
        pages = pages.text.strip()
        y = pages[10]
        y = int(y) + 1
        list_page = []
        
        for i in range(1, y):
            list_page.append(category_url.replace('index.html','') + f'page-{i}.html')
        
        return list_page

    else:
        list_page = [category_url]
        
        return list_page
   
# Get books url from all category pages
def extract_books_url(soup):
    """
    Get all the product_url from the full category
    """
    
    list_url = []
    h3 = soup.find('ol', class_='row').find_all('h3')
    
    for h in h3:
        a = h.find('a')
        href = a['href'].replace('../../../','https://books.toscrape.com/catalogue/')
        list_url.append(href)

    return list_url
        
# Get data from a book
def extract_data(soup):
    """
    Extract data from the book's url
    """
    
    table = soup.find('table', {'class' : 'table table-striped'})

    data = {}
    data['product_page_url'] = product_url
    data['upc'] = table.find('td').text
    data['title'] = soup.find('div', {'class' : 'col-sm-6 product_main'}).find('h1').text.replace(',',';')
    data['price_including_tax'] = table.find('th', text = 'Price (incl. tax)').find_next_sibling('td').text.replace('Â','')
    data['price_excluding_tax'] = table.find('th', text = 'Price (excl. tax)').find_next_sibling('td').text.replace('Â','')
    data['number_available'] = table.find('th', text = 'Availability').find_next_sibling('td').text
    
    description = soup.find('div', {'id' : 'product_description'})
    if description is not None:
        data['product_description'] = description.find_next_sibling('p').text.replace(',',';')
    else:
        data['product_description'] = ''
    

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
 
# Write Data in the .csv file
def write_data_csv(data,f):
    with open(category_name, 'a') as f:
        f.write(data['product_page_url'] + ',' + data['upc'] + ',' + data['title'] 
        + ',' + data['price_including_tax'] + ',' + data['price_excluding_tax']
        + ',' + data['number_available'] + ',' + data['product_description']
        + ',' + data['category'] + ',' + data['review_rating'] 
        + ',' + data['image_url'] + '\n')

# Save img in the directory           
def save_img(img_url):
    res = requests.get(img_url, stream =  True)
    # img_name = data['title'] + '.png'.replace('/', '-')
    img_name = f"{data['title']}.png".replace('/', '-')
    if res.ok:
        with open(img_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        

if __name__ == '__main__':

    url = 'https://books.toscrape.com/'
    soup = extract_html(url)
    list_categories = extract_category(soup)
    state = 1
    for category_url in list_categories:
        soup_category = extract_html(category_url)
        list_page = extract_pages_category(soup_category)
        
        category_name = category_url.replace('https://books.toscrape.com/catalogue/category/books/','').replace('/index.html','') + '.csv'
        with open(category_name, 'w') as f:
            column ='product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n'
            f.write(column)

        for page in list_page:
            soup_page = extract_html(page)
            list_product_url = extract_books_url(soup_page)
    
            for product_url in list_product_url:
                soup_product = extract_html(product_url)
                data = extract_data(soup_product)
                save_img(data['image_url'])
                write_data_csv(data,f)
                
                print('State :' + str(state))
                state = state + 1
        
    print('Job done !')


   

    

