import os
import requests
import get_vacancy_lists
# import json
# import bs4
import csv

# import html5lib
# import vacancy_parse_html
# import vacancy_parse_json

TOKEN = 'APPLO6JGASGHDGAG3I55G20UKG4G002H99V58VBDU6JCKCTGE2P3OD3EUAP4A6IM'
AREAS = 'areas'
ID = 'id'
NAME = 'name'

FILE_NAME = f'{AREAS}/{AREAS}.csv'
VACANCY_DIR = './vacancy'

VACANCY_COLUMNS = [
    'id',
    'name',
    'url',
    'employment_id',
    'employment_name',
    'salary_from',
    'salary_to',
    'snippet_requirement',
    'snippet_responsibility',
    'experience_id',
    'experience_name',
    'employer_id',
    'employer_name',
    'address_lat',
    'address_lng',
    'professional_roles_id',
    'professional_roles_name'
]


def get_areas_array(json_response):
    if AREAS in json_response:
        areas_array = json_response[AREAS]
        result_areas = []

        for index in range(0, len(areas_array)):
            area = {
                ID: str(areas_array[index][ID]).encode('cp1251', errors='ignore').decode('cp1251'),
                NAME: str(areas_array[index][NAME]).encode('cp1251', errors='ignore').decode('cp1251'),
            }

            result_areas.append(area)

        print(result_areas)

        return result_areas


def get_areas(area_id):
    headers = {
        "Authorization": "Bearer " + TOKEN
    }

    r = requests.get(f'https://api.hh.ru/{AREAS}/{area_id}/', headers=headers)
    if r.status_code == requests.codes.ok:
        print('response', r.json())
        areas = get_areas_array(r.json())

        os.mkdir(f'./{AREAS}')

        with open(FILE_NAME, 'w+', encoding='cp1251', newline='') as file:
            columns = [ID, NAME]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(areas)

    else:
        print('Something goes wrong')


# get_areas('1948')

def main_loop(file_name):
    print('START')

    search_data = []

    with open(file_name, 'r', encoding='cp1251', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = {
                ID: row[ID],
                NAME: row[NAME],
            }
            search_data.append(data)

    print(f'SEARCH: {search_data}')
    os.mkdir(VACANCY_DIR)

    for row in search_data:
        print(f'ID: {row[ID]}, AREA: {row[NAME]}')
        result = get_vacancy_lists.get_vacancies(row[ID], row[NAME])
        print(f'len result: {len(result)}')

        if 0 == len(result):
            continue
        else:
            current_file = f'{VACANCY_DIR}/{row[ID]}_{row[NAME]}.csv'

            with open(current_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=VACANCY_COLUMNS)
                writer.writeheader()

                writer.writerows(result)

    print('FINISH')


# main_loop(FILE_NAME)

EMPLOYMENT_ID = 'employment_id'
COUNT = 'count'

HEADER_EMPLOYMENT_ID_COUNT = [
    COUNT,
    EMPLOYMENT_ID
]


def get_count_table_by_param(file_name, param, count, output_file_name, header):
    array_of_dict = []

    with open(file_name, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row[param] is not None:
                is_exist = False

                for current_row in array_of_dict:
                    if current_row[param] == row[param]:
                        is_exist = True

                        current_row[count] += 1

                if not is_exist:
                    new_row = {
                        param: row[param],
                        count: 1
                    }

                    array_of_dict.append(new_row)

    with open(output_file_name, 'w', encoding='cp1251', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        writer.writerows(array_of_dict)


get_count_table_by_param('./all-vacancy-with-area.csv', 'experience_name', COUNT,
                         'count_vacancy_from_experience_name.csv',
                         ['experience_name', COUNT])
get_count_table_by_param('./all-vacancy-with-area.csv', 'employment_name', COUNT,
                         'count_vacancy_from_employment_name.csv',
                         ['employment_name', COUNT])
get_count_table_by_param('./all-vacancy-with-area.csv', 'employer_name', COUNT, 'count_vacancy_from_employer_name.csv',
                         ['employer_name', COUNT])
