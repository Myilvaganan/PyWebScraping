from bs4 import BeautifulSoup

import requests
import time

def searchForJobs():
    url = "https://www.linkedin.com/jobs/search?keywords=React.js&location=India&locationId=&geoId=102713980&f_TPR=&f_PP=115702354%2C105214831%2C116703352&position=1&pageNum=0"
    html_request_text = requests.get(url).text
    soup = BeautifulSoup(html_request_text, 'lxml')
    jobs = soup.find_all('div', class_='base-search-card__info')
    for index, job in enumerate(jobs):
        jobLink = job.a.get('href')
        location = job.div.span.text
        companyName = job.h4.text
        jobTitle = job.h3.text
        timeDate = job.div.time.get('datetime')
        with open(f'jobPosts/{index+1}.txt', 'w') as f:
            f.write(f'CompanyName: {companyName.strip()}')
            f.write(f'Job Title: {jobTitle.strip()}')
            f.write(f'Location: {location.strip()}')
            f.write(f'Posted On: {timeDate.strip()}')
            f.write(f'Link: {jobLink.strip()}')
        print(f'File Saved in: {index+1}')

if __name__ == '__main__':
    while True:
        searchForJobs()
        time_wait = 1
        print(f'Waiting {time_wait} minute...')
        time.sleep(time_wait * 60)


