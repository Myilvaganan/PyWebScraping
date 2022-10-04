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
WEBSITE_URL = "https://www.flipkart.com"

# Crawling Top Offers from the Flipkart website


def scraping_flipkart():
    try:
        response = requests.get(SAREES_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('div', class_='_1xHGtK')
        product_list = {'product_id': [], 'product_link': [], 'product_name': [], 'product_offer_price': [], 'product_strike_price': [], 'product_extra_info': []}
        for index, product in enumerate(data):
            product_link = WEBSITE_URL + product.find('a', class_="_2UzuFa").get('href')
            product_name = product.find('a', class_="IRpwTa").get_text(strip=True)
            offer_price = product.find('div', class_="_30jeq3").text
            strike_price = product.find('div', class_="_3I9_wc").text
            offer_percentage = product.find('div', class_="_3Ay6Sb").findNext('div').text
            rowId = index + 1
            product_list['product_id'].append(str(rowId))
            product_list['product_link'].append(product_link)
            product_list['product_name'].append(product_name)
            product_list['product_offer_price'].append(offer_price)
            product_list['product_strike_price'].append(strike_price)
            product_list['product_extra_info'].append(offer_percentage)
    except Exception as error:
        print(error)

    dataFrame = pandas.DataFrame(data=product_list)
    connection = sqlite3.connect("web_scraping_flipkart.db")
    cursor=connection.cursor()
    query="CREATE TABLE IF NOT EXISTS sarees(product_id,product_link,product_name,product_offer_price,product_strike_price,product_extra_info)"
    cursor.execute(query)
    for i in range(len(dataFrame)):
        cursor.execute("INSERT INTO sarees values (?,?,?,?,?,?)", dataFrame.iloc[i])

    connection.commit()
    connection.close()

    # excel.save("FlipKart_Scraped_Data.xlsx")


scraping_flipkart()
