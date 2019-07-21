import re

from pprint import pprint as print
from requests_html import HTMLSession

session = HTMLSession()
print(session)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Cookie': 'sp-cdn="L5Z9:UY"'
}


def product_data(product_id):
    response = session.get(f'https://www.amazon.com/dp/{product_id}/', headers=header)
    print(response)
    try:
        product = response.html.find('#productTitle', first=True).text
        print(f'Product: {product}')
        try:
            price = float(response.html.find('.a-size-base.a-color-base')[0].text[1:])
            print(f'Price: {price}')
            shipping = float(response.html.find('.a-size-base.a-color-base')[1].text[1:])
            print(f'Shipping: {shipping}')
            taxes = float(response.html.find('.a-size-base.a-color-base')[2].text[1:])
            print(f'Taxes: {taxes}')
            tax_percentage = int(round(taxes / price * 100, 0))
            print(f'Tax percentage: {tax_percentage}%')
        except ValueError:
            print('Could not scrape this item')
    except AttributeError:
        print('Not a product')


#product_data('B07GCL6BR4')
#product_data('B0781Z7Y3S')
#product_data('B07H2F3741')

response = session.get('https://www.amazon.com/s?i=computers&bbn=1292116011&rh=n%3A172282%2Cn%3A493964%2Cn%3A541966%2Cn%3A1292110011%2Cn%3A1292116011%2Cp_36%3A20000-&dc&qid=1563664831&rnid=16354392011&ref=sr_nr_p_n_global_store_origin_marketplace_1', headers=header)
print(response)
ssds = response.html.find('[href*="/dp/"]')
print(response.html.html)
print(ssds)
for ssd in ssds:
    product_id = re.findall('/dp/(\w.*)\?', ssd.attrs['href'])
    print(product_id)
    product_data(product_id)

# https://html.python-requests.org/
# https://www.w3schools.com/cssref/css_selectors.asp
