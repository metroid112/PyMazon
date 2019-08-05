import re

from pprint import pprint as print
from requests_html import HTMLSession

session = HTMLSession()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Cookie': 'sp-cdn="L5Z9:UY"'
}


def product_data(product_id):
    global products
    product_response = session.get(f'https://www.amazon.com/dp/{product_id}/', headers=header)
    try:
        product_name = product_response.html.find('#productTitle', first=True).text
        try:
            price = float(product_response.html.find('.a-size-base.a-color-base')[0].text[1:])
            shipping = float(product_response.html.find('.a-size-base.a-color-base')[1].text[1:])
            taxes = float(product_response.html.find('.a-size-base.a-color-base')[2].text[1:])
            tax_percentage = int(round(taxes / price * 100, 0))
            products.append([product_name, price, shipping, taxes, tax_percentage])
        except ValueError as exception:
            print(f'Could not scrape this item: {exception}')
    except AttributeError as exception:
        print(f'Not a product: {exception}')


response = session.get('https://www.amazon.com/s?i=specialty-aps&bbn=16225007011&rh=n%3A16225007011%2Cn%3A193870011&_encoding=UTF8&ref=sd_allcat_nav_desktop_sa_intl_computer_components', headers=header)
html_file = open('a.html', 'w')
html_file.write(str(response.html.html.encode('ascii', 'ignore')))
html_file.close()
links = response.html.search_all('<a class="a-link-normal a-text-normal" href="{href}">')
print(links)
products = []
for link in links:
    product_id = re.findall('/dp/(\\w.*)/', link['href'])[0]
    product_data(product_id)
print('************************')
for product in products:
    if product[4] < 60:
        print(f'Product {product[0]} is worth! (tax rate is {product[4]}%) {product[1]}$')
