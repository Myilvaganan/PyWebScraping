# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from bs4 import BeautifulSoup

# To read the html file - 'r' ; as - used to keep alias
# read() function to read the content in the file
with open('home.html','r') as demoHTML:
    content = demoHTML.read()
    soup = BeautifulSoup(content, 'lxml')
    # Print the html tags in the specified format
    # print(soup.prettify())

    # Find the specific tags
    # find will find the first occurrences
    # findAll give all the items which are queried
    tags = soup.find('h5')
    allTags = soup.findAll('h5')
    allTags2 = soup.find_all('h5')

    # Reading the content inside all queried tags
    # for tag in allTags2:
       # print(tag.text)

    # Getting all the course cards
    course_cards = soup.find_all('div', class_ = 'card')
    for card in course_cards:
       course_name = card.h5.text
       course_price = card.a.text.split()[-1]
       print(course_name + " = " + course_price)
