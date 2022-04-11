import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = 'https://www.diversual.com/'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}

product_links = []
for x in range(1,10):
    r = requests.get(f'https://www.diversual.com/es/43-lubricantes?p={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    product_list = soup.find_all('div', class_='product-container')
    for item in product_list:
        product_links.append(item.a['href'])

product_list_lubricantes = []
for link in product_links:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', itemprop='name').text.strip()

    try:
        brand = soup.find('h2', class_='fabric').text.strip()
    except AttributeError as err:
        brand = 'None'

    reference = soup.find('span', class_='editable').text.strip()

    try:
        rating = soup.find('li', class_='current-rating').text.strip()
    except AttributeError as err:
        rating = 'None'
    try:
        comments = soup.find('div', class_='valoracion').text.strip()
    except AttributeError as err:
        comments = 'None'

    price = soup.find('span', id='our_price_display').text.strip()

    try:
        old_price = soup.find('p', id="old_price").text.strip()
    except AttributeError as err:
        old_price = 'None'


    product_url = link

    product = {
        'Nombre': name,
        'Fabricante': brand,
        'Referencia': reference,
        'Rating': rating,
        'Valoraciones': comments,
        'Precio Actual': price,
        'Precio Antes': old_price,
        'URL': product_url
    }

    product_list_lubricantes.append(product)
    print('Savings: ', product['Nombre'])

df = pd.DataFrame(product_list_lubricantes)
df.to_csv('diversual_lubricantes.csv', index=False)
# print(df.head(15))






