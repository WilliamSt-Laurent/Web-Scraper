import string
import os
import requests
from bs4 import BeautifulSoup

# url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"

number_of_pages = int(input())
selected_type = input()

current_dir = os.getcwd()

for page in range(1, number_of_pages + 1):
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    # parameters = {'searchType': 'journalSearch', 'sort': 'PubDate', 'year': '2020', 'page': f'{page}'}
    parameters = {'page': f'{page}'}

    # Preparing the URL
    r = requests.get(url, parameters)
    page_content = r.content
    status_code = r.status_code

    # Creating the file
    os.chdir('/Users/williamst-laurent/PycharmProjects/Web Scraper/Web Scraper/task')
    directory = os.mkdir(f'Page_{page}')
    os.chdir(f'Page_{page}')

    soup = BeautifulSoup(page_content, 'html.parser')
    articles = soup.findAll('article')

    for article in articles:
        article_type = article.findAll('span', {'class': 'c-meta__type'})

        for type in article_type:
            if type.text == selected_type:
                url = "https://www.nature.com"
                parameter = article.find('a').get('href')

                article_page = requests.get(url + parameter).content
                article_soup = BeautifulSoup(article_page, 'html.parser')
                title = article_soup.title.text
                article_body = article_soup.find('p', {'class': 'article__teaser'}).text
                # article_body = article_soup.find('p').text

                punctuation = list(string.punctuation)
                file_name = title
                for char in punctuation:
                    file_name = file_name.replace(char, "")
                formatted_file_name = file_name.replace(" ", "_")

                my_file = open(f'{formatted_file_name}.txt', 'w', encoding='utf-8')
                my_file.write(article_body)
                my_file.close()

                # print(formatted_file_name)
