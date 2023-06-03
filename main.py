import requests
import bs4
import csv
import html5lib
import vacancy_parse_html
import vacancy_parse_json


# Главный цикл обработки ссылок вакансий
def main_cycle(FILE_NAME):
    file_links = open('test_parse.txt', 'r')
    all_links = file_links.readlines()

    for link_number in range(0, len(all_links)):
        document = get_html_document(all_links[link_number])

        soup = bs4.BeautifulSoup(document, 'html5lib')
        # print(soup.prettify())

        if not check_is_valid_document(document):
            print('something wrong')
            continue

        vacancy = parsing_doc(document)

        file = open(FILE_NAME, 'w', newline="")
        columns = ['vacancy', 'salary', 'city', 'employment', 'professionalArea', 'experience', 'education',
                  'driver_license_category']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow(vacancy)
        file.close()

        print('write vacancy')


# Получить html документ
def get_html_document(url):
    response = requests.get(f'{url}')
    html_doc = response.text

    return html_doc


# Проверить валидность документа на нужный тег
def check_is_valid_document(document):
    soup = bs4.BeautifulSoup(document, 'html5lib')

    vacancy_raw = soup.find('span', {'class': 'inplace', 'data-field': 'type'})
    if vacancy_raw:
        return True
    else:
        return False


# Распарсить документ
def parsing_doc(document):
    dict_html_info = vacancy_parse_html.parse_html(document)
    dict_json_info = vacancy_parse_json.parse_json(document)

    vacancy_info = {}
    for key, value in dict_json_info.items():
        vacancy_info[key] = value

    for key, value in dict_html_info.items():
        vacancy_info[key] = value

    return vacancy_info


FILE_NAME = 'vacancy.csv'

file = open(FILE_NAME, 'w', newline="")
columns = ['vacancy', 'salary', 'city', 'employment', 'professionalArea', 'experience', 'education', 'driver_license_category']
writer = csv.DictWriter(file, fieldnames=columns)
writer.writeheader()
file.close()

main_cycle(FILE_NAME)

# file = open(FILE_NAME, 'w', newline="")
# columns = ['vacancy', 'salary', 'city', 'employment', 'professionalArea', 'experience', 'education', 'driver_license_category']
# reader = csv.DictReader(file)
# for row in reader:
#     print(row['title'])
# file.close()
