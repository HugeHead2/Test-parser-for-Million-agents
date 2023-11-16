import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_metro_products(category_url):
    base_url = "https://online.metro-cc.ru/category"
    product_url = "https://online.metro-cc.ru"

    result_data = []

    for i in range(7):
        url = f"{base_url}/{category_url}?page={i+1}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='product-card')

            len(products)

            for product in products:
                product_id = product.get('data-sku')
                name = product.find('a', class_='product-card-name').text.strip()
                link = product_url + product.find('a', class_='product-card-name').get('href')
                regular_price = product.find('div', class_='product-unit-prices__old-wrapper').text.strip().split(' ')[0].replace('\\xa','')
                promo_price_tag = product.find('div', class_='product-unit-prices__actual-wrapper')
                promo_price = promo_price_tag.text.strip().split(' ')[0].replace('\\xa','')

                if regular_price == '':
                    regular_price = promo_price
                    promo_price = ''

                response_product_page = requests.get(link)
                brand = BeautifulSoup(response_product_page.text, 'html.parser').find_all('a', class_='product-attributes__list-item-link')[0].text.strip()

                availability = product.find('button', class_='product-availability-status').text.strip()
                if availability.lower() == "нет в наличии":
                    continue

                product_data = {
                'id': product_id,
                'name': name,
                'link': link,
                'regular_price': regular_price,
                'promo_price': promo_price,
                'brand': brand
                }

                result_data.append(product_data)

        else:
            print(f"Ошибка {response.status_code} при обращении к {url}")
            return None
    return result_data

def parse_metro_products_to_json():
    data = get_metro_products("myasnye/kolbasy-vetchina")
    df = pd.DataFrame(data)
    df.to_csv("requirements.csv")


if __name__ == '__main__':
    parse_metro_products_to_json()

