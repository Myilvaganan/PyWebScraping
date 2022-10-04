import uuid

import openpyxl
from bs4 import BeautifulSoup
import requests
import pandas
import sqlite3

# excel = openpyxl.Workbook()
# sheet = excel.active
# sheet.title = "Tshirt Flipkart"
# sheet.append(['S.No', 'Product Link', 'Product Name', 'Offer Price', 'Strike Price', 'Extra Info'])
SHIRTS_URL = "https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank," \
             "edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts "
SAREES_URL = "https://www.flipkart.com/clothing-and-accessories/saree-and-accessories/saree/women-saree/pr?sid=clo," \
             "8on,zpd,9og&otracker=categorytree&otracker=nmenu_sub_Women_0_Sarees "
T_SHIRTS_URL = "https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&otracker[]=categorytree&otracker[" \
               "]=nmenu_sub_Men_0_T-Shirts&page="
WEBSITE_URL = "https://www.flipkart.com"


# Crawling Top Offers from the Flipkart website


def scraping_flipkart(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('div', class_='_1xHGtK')
        product_list = {'product_id': [], 'product_link': [], 'product_name': [], 'product_offer_price': [], 'product_strike_price': [], 'product_extra_info': []}
        for index, product in enumerate(data):
            product_link = WEBSITE_URL + product.find('a', class_="_2UzuFa").get('href')
            product_name = product.find('a', class_="IRpwTa").get_text(strip=True)
            offer_price = product.find('div', class_="_30jeq3").text
            strike_price = product.find('div', class_="_3I9_wc").text
            offer_percentage = product.find('div', class_="_3Ay6Sb").findNext('div').text
            rowId = uuid.uuid4()
            product_list['product_id'].append(str(rowId))
            product_list['product_link'].append(product_link)
            product_list['product_name'].append(product_name)
            product_list['product_offer_price'].append(offer_price)
            product_list['product_strike_price'].append(strike_price)
            product_list['product_extra_info'].append(offer_percentage)
    except Exception as error:
        print(error)

    dataFrame = pandas.DataFrame(data=product_list)
    connection = sqlite3.connect("WEB_SCRAPING_FLIPKART.db")
    cursor = connection.cursor()
    query = "CREATE TABLE IF NOT EXISTS tshirts(product_id,product_link,product_name,product_offer_price,product_strike_price,product_extra_info,PRIMARY KEY (product_id))"
    cursor.execute(query)
    for i in range(len(dataFrame)):
        cursor.execute("INSERT INTO tshirts values (?,?,?,?,?,?)", dataFrame.iloc[i])

    connection.commit()
    connection.close()

    # excel.save("FlipKart_Scraped_Data.xlsx")


page_no = 0
for page in range(0, 20):
    page_no = page + 1
    URL = T_SHIRTS_URL + str(page_no)
    scraping_flipkart(URL)
