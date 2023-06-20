import requests

TOKEN = 'APPLO6JGASGHDGAG3I55G20UKG4G002H99V58VBDU6JCKCTGE2P3OD3EUAP4A6IM'
AREAS = 'areas'
AREA = 'area'
ID = 'id'
NAME = 'name'
FOUND = 'found'
ITEMS = 'items'

FILE_NAME = f'{AREAS}/{AREAS}.csv'
VACANCY_DIR = './vacancy'


# Добавить обработку случаев с 0 полями
def append_to_array_vacancies(result, items):
    for index in range(0, len(items)):
        vacancy = {
            'id': items[index]['id'],
            'name': items[index]['name'],
            'url': items[index]['apply_alternate_url'],
            'snippet_requirement': items[index]['snippet']['requirement'],
            'snippet_responsibility': items[index]['snippet']['responsibility'],
            'experience_id': items[index]['experience']['id'],
            'experience_name': items[index]['experience']['name'],
            'employment_id': items[index]['employment']['id'],
            'employment_name': items[index]['employment']['name'],
        }

        if 'salary' in items[index] and None != items[index]['salary']:
            if 'from' in items[index]['salary'] and 'to' in items[index]['salary']:
                vacancy['salary_from'] = items[index]['salary']['from']
                vacancy['salary_to'] = items[index]['salary']['to']
            else:
                vacancy['salary_from'] = 'null'
                vacancy['salary_to'] = 'null'
        else:
            vacancy['salary_from'] = 'null'
            vacancy['salary_to'] = 'null'

        if 'employer' in items[index] and None != items[index]['employer']:
            if 'id' in items[index]['employer'] and 'name' in items[index]['employer']:
                vacancy['employer_id'] = items[index]['employer']['id']
                vacancy['employer_name'] = items[index]['employer']['name']
            else:
                vacancy['employer_id'] = 'null'
                vacancy['employer_name'] = 'null'
        else:
            vacancy['employer_id'] = 'null'
            vacancy['employer_name'] = 'null'

        if 'address' in items[index] and None != items[index]['address']:
            if 'lat' in items[index]['address'] and 'lng' in items[index]['address']:
                vacancy['address_lat'] = items[index]['address']['lat']
                vacancy['address_lng'] = items[index]['address']['lng']
            else:
                vacancy['address_lat'] = 'null'
                vacancy['address_lng'] = 'null'
        else:
            vacancy['address_lat'] = 'null'
            vacancy['address_lng'] = 'null'

        if 'professional_roles' in items[index] and None != items[index]['professional_roles']:
            if 'id' in items[index]['professional_roles'] and 'name' in items[index]['professional_roles']:
                vacancy['professional_roles_id'] = items[index]['professional_roles']['id']
                vacancy['professional_roles_name'] = items[index]['professional_roles']['name']
            else:
                vacancy['professional_roles_id'] = 'null'
                vacancy['professional_roles_name'] = 'null'
        else:
            vacancy['professional_roles_id'] = 'null'
            vacancy['professional_roles_name'] = 'null'

        print('vacancy', vacancy)
        result.append(vacancy)

    return result


def get_vacancies(area_id, area_name):
    print('area_name', area_name)

    headers = {
        "Authorization": "Bearer " + TOKEN
    }

    result = []

    r = requests.get(f'https://api.hh.ru/vacancies?{AREA}={area_id}&per_page=100&page=0', headers=headers)

    if r.status_code == requests.codes.ok:
        json_data = r.json()

        if 100 >= json_data[FOUND]:
            items = json_data[ITEMS]

            result.extend(append_to_array_vacancies(result, items));

        else:
            items = json_data[ITEMS]

            result.extend(append_to_array_vacancies(result, items))

            cycle_count = json_data['pages']

            for index in range(0, cycle_count):
                r_cycle = requests.get(f'https://api.hh.ru/vacancies?{AREA}={area_id}&per_page=100&page={index + 1}',
                                       headers=headers)

                if r.status_code != requests.codes.ok:
                    continue

                json_cycle_data = r_cycle.json()

                items_cycle = json_cycle_data[ITEMS]

                result.extend(append_to_array_vacancies(result, items_cycle))

        return result

    return result
