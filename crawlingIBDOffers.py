from bs4 import BeautifulSoup
import requests
import pandas
import sqlite3
import uuid

T_SHIRTS_URL = "https://www.flipkart.com/mens-tshirts/pr?sid=clo%2Cash%2Cank%2Cedy&otracker[]=categorytree&otracker[" \
               "]=nmenu_sub_Men_0_T-Shirts&page="
WEBSITE_URL = "https://www.flipkart.com"
SAMPLE_TEXT = "https://www.flipkart.com/damensch-solid-men-polo-neck-yellow-t-shirt/p/itma9bce5f633b9d?pid" \
              "=TSHG9G9TZHPDQFY9&lid=LSTTSHG9G9TZHPDQFY9MX6ROV&marketplace=FLIPKART&store=clo%2Fash%2Fank%2Fedy&srno" \
              "=b_1_1&otracker=browse&iid=en_W7UBdD6Ec8PmEU3TV2BTUJLLh7ZyGk6Xg38nVQW2014UHD" \
              "%2B9cB9OvTJJEhs056yY2tW1yZbcJlWwd7BoAHCYng%3D%3D&ssid=o50fadgwei5712ww1664876468210 "

html_parser = 'html.parser'
href_attribute = 'href'
anchor_tag = 'a'
div_tag = 'div'
list_tag = 'li'
class_name_for_data_wrapper = '_1xHGtK'
class_name_for_product_link = '_2UzuFa'
class_name_for_product_name = 'IRpwTa'
class_name_for_product_price = '_30jeq3'
class_name_for_strike_price = '_3I9_wc'
class_name_for_more_info = '_3Ay6Sb'
class_name_for_ibd_offer_data = '_16eBzU'
product_list = {'product_id': [], 'product_link': [], 'product_name': [], 'product_offer_price': [],
                'product_strike_price': [], 'product_extra_info': []}
ibd_list = {'ibd_id': [], 'offer_type': [], 'offer_title': [], 'product_id': []}


def updateInSQLData():
    dataFrame = pandas.DataFrame(data=product_list)
    dataFrame2 = pandas.DataFrame(data=ibd_list)
    connection = sqlite3.connect("flipkart_ibd_offer_master.db")
    cursor = connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS products(product_id,product_link,product_name,product_offer_price,product_strike_price,product_extra_info,PRIMARY KEY (product_id))'
    ibd_query = 'CREATE TABLE IF NOT EXISTS ibd_offers(ibd_id,offer_type,offer_title,product_id,PRIMARY KEY (ibd_id),FOREIGN KEY (product_id) REFERENCES products(product_id))'
    cursor.execute(query)
    cursor.execute(ibd_query)
    for i in range(len(dataFrame)):
        cursor.execute("INSERT or REPLACE INTO products values (?,?,?,?,?,?)", dataFrame.iloc[i])
    for i in range(len(dataFrame2)):
        cursor.execute("INSERT or REPLACE INTO ibd_offers values (?,?,?,?)", dataFrame2.iloc[i])
    connection.commit()
    connection.close()


def getIBDOffers(link, row_id):
    try:
        if link:
            crawled_data = requests.get(link)
            html_parsed = BeautifulSoup(crawled_data.text, html_parser)
            ibd_data = html_parsed.find_all(list_tag, class_=class_name_for_ibd_offer_data)
            for i in ibd_data:
                headerSpanWrapper = i.find('span', class_='u8dYXW')
                if headerSpanWrapper.text:
                    offer_header = headerSpanWrapper.text
                    offer_title = headerSpanWrapper.find_next_sibling('span').text
                else:
                    offer_header = i.find('span').text
                    offer_title = ""
                ibd_id = uuid.uuid4()
                ibd_list['ibd_id'].append(str(ibd_id))
                ibd_list['offer_type'].append(offer_header)
                ibd_list['offer_title'].append(offer_title)
                ibd_list['product_id'].append(str(row_id))
                updateInSQLData()
    except Exception as error:
        print(error)


# Crawling Top Offers from the Flipkart website


def scraping_flipkart(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, html_parser)
        data = soup.find_all(div_tag, class_=class_name_for_data_wrapper)

        for index, product in enumerate(data):
            product_link = WEBSITE_URL + product.find(anchor_tag, class_=class_name_for_product_link).get(
                href_attribute)
            product_name = product.find(anchor_tag, class_=class_name_for_product_name).get_text(strip=True)
            offer_price = product.find(div_tag, class_=class_name_for_product_price).text
            strike_price = product.find(div_tag, class_=class_name_for_strike_price).text
            more_info = product.find(div_tag, class_=class_name_for_more_info).findNext(div_tag).text
            rowId = uuid.uuid4()
            product_list['product_id'].append(str(rowId))
            product_list['product_link'].append(product_link)
            product_list['product_name'].append(product_name)
            product_list['product_offer_price'].append(offer_price)
            product_list['product_strike_price'].append(strike_price)
            product_list['product_extra_info'].append(more_info)
            getIBDOffers(product_link, str(rowId))
    except Exception as error:
        print(error)


page_no = 0
for page in range(0, 20):
    page_no = page + 1
    URL = T_SHIRTS_URL + str(page_no)
    scraping_flipkart(URL)
