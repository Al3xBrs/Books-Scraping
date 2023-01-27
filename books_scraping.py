import requests
from bs4 import BeautifulSoup

category_url ='https://books.toscrape.com/catalogue/category/books/young-adult_21/'

# Get number of page from a category
def extract_pages_category(category_url):
    """
    Extract all pages from the category
    """

    response = requests.get(category_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print('Category_Url Error code : ' + str(response))

    pages = soup.find('li', class_='current').text.strip()
    y = pages[10]
    y = int(y) + 1
    list_page = []
    
    for i in range(1, y):
        list_page.append(category_url + f'page-{i}.html')
    
    return list_page

# Get books url from all category pages
def extract_books_url(list_page):
    """
    Get all the product_url from the full category
    """

    list_url = []
    for page in list_page:
        response = requests.get(page)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
        h3 = soup.find('ol', class_='row').find_all('h3')
        for h in h3:
            a = h.find('a')
            href = a['href'].replace('../../../','https://books.toscrape.com/catalogue/')
            list_url.append(href)

    return list_url
        
# Get data from a book
def extract_data(product_url):
    """
    Extract data from the book's url
    """
    
    response = requests.get(product_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print('Product_Url Error code :' + str(response))
    
    table = soup.find('table', {'class' : 'table table-striped'})

    data = {}
    data['product_page_url'] = product_url
    data['upc'] = table.find('td').text
    data['title'] = soup.find('div', {'class' : 'col-sm-6 product_main'}).find('h1').text.replace(',',';')
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
 
if __name__ == '__main__':
    list_page = extract_pages_category(category_url)
    list_url = extract_books_url(list_page)
    
    #Write data in .csv file
    with open('books.csv', 'w') as f:
        column ='product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url\n'
        f.write(column)
        for product_url in list_url:
            data = extract_data(product_url)
            f.write(data['product_page_url'] + ',' + data['upc'] + ',' + data['title'] 
            + ',' + data['price_including_tax'] + ',' + data['price_excluding_tax']
            + ',' + data['number_available'] + ',' + data['product_description']
            + ',' + data['category'] + ',' + data['review_rating'] 
            + ',' + data['image_url'] + '\n')
            print(data['title'])

    print('Job done !')


   

    

