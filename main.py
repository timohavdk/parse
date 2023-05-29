import requests
import bs4
import html5lib


def get_html_page(page_number):
    response = requests.get(f'https://www.farpost.ru/rabota/vacansii/?page={page_number}')
    #response = requests.get('https://www.farpost.ru//khabarovsk/rabota/vacansii/administrator-kassir-v-kafe-21393606.html')
    html_doc = response.text
    print(html_doc)

    return html_doc


def get_vacancy_links(document):
    soup = bs4.BeautifulSoup(document, 'html5lib')
    raw_links = soup.find_all('a', class_="bull-item__self-link")

    link = []

    for i in range(0, len(raw_links)):
        a_link = raw_links[i]

        link.append('https://www.farpost.ru' + a_link.get('href'))

    return link


def search_cycle(pages_counts):
    for page_number in range(200, pages_counts):
        document = get_html_page(page_number)

        links = get_vacancy_links(document)

        for i in range(0, len(links)):
            print('link', links[i])
            file = open('clear2.txt', 'a')
            file.write(links[i] + '\n')
            file.close()



search_cycle(400)

#get_html_page(1)
