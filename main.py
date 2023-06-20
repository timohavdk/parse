import os
import requests
import get_vacancy_lists
import json
import bs4
import csv
import html5lib
import vacancy_parse_html
import vacancy_parse_json

TOKEN = 'APPLO6JGASGHDGAG3I55G20UKG4G002H99V58VBDU6JCKCTGE2P3OD3EUAP4A6IM'
AREAS = 'areas'
ID = 'id'
NAME = 'name'

FILE_NAME = f'{AREAS}/{AREAS}.csv'
VACANCY_DIR = './vacancy'


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
    with open(file_name, 'r+', encoding='cp1251', newline='') as file:
        reader = csv.DictReader(file)

        limit = 0

        for row in reader:
            result = get_vacancy_lists.get_vacancies(row[ID], row[NAME])

            #сделать запись в csv файлы
            print('result', result)

            limit += 1

            if 0 == len(result):
                continue

            if limit > 4:
                break


main_loop(FILE_NAME)
