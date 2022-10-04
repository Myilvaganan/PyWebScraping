from bs4 import BeautifulSoup

import requests
import time

import scrapingFlipkart


def searchForJobs():
    url = "https://www.linkedin.com/jobs/search?keywords=React.js&location=India&locationId=&geoId=102713980&f_TPR=&f_PP=115702354%2C105214831%2C116703352&position=1&pageNum=0"
    # Getting data from the above link
    html_request_text = requests.get(url).text
    soup = BeautifulSoup(html_request_text, 'lxml')
    jobs = soup.find_all('div', class_='base-search-card__info')
    for index, job in enumerate(jobs):
        jobLink = job.a.get('href')
        location = job.div.span.text
        companyName = job.h4.text
        jobTitle = job.h3.text
        timeDate = job.div.time.get('datetime')
        with open(f'jobPosts/{index + 1}.txt', 'w') as f:
            f.write(f'CompanyName: {companyName.strip()}')
            f.write(f'Job Title: {jobTitle.strip()}')
            f.write(f'Location: {location.strip()}')
            f.write(f'Posted On: {timeDate.strip()}')
            f.write(f'Link: {jobLink.strip()}')
        print(f'File Saved in: {index + 1}')


def crawl1mgWebsite():
    header = {
        'Origin': 'https://www.1mg.com',
        'Referer': 'https://www.1mg.com/categories/exclusive/immunity-boosters/vitamin-c-734',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36 '
    }
    url = 'https://www.1mg.com/categories/exclusive/immunity-boosters/vitamin-c-734'
    html = requests.get(url=url, headers=header).text
    bs_obj = BeautifulSoup(html, 'lxml')
    product_name = []
    for name in bs_obj.findAll('div', class_='style__pro-title___2QwJy'):
        product_name.append(name.text.strip())
    return product_name


"""
if __name__ == '__main__':
    while True:
        searchForJobs()
        print(crawl1mgWebsite())
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60) 
"""


if __name__ == '__main__':
    while True:
        scrapingFlipkart.scraping_flipkart()
