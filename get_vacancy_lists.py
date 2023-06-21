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


def write_properties(result_dictionary, target_dictionary, property_name, first_child, second_child):
    if property_name in target_dictionary and target_dictionary[property_name] is not None:
        first_cond = f'{first_child}' in target_dictionary[f'{property_name}']
        second_cond = f'{second_child}' in target_dictionary[property_name]
        if first_cond and second_cond:
            result_dictionary[f'{property_name}_{first_child}'] = target_dictionary[property_name][f'{first_child}']
            result_dictionary[f'{property_name}_{second_child}'] = target_dictionary[property_name][f'{second_child}']
        else:
            result_dictionary[f'{property_name}_{first_child}'] = None
            result_dictionary[f'{property_name}_{second_child}'] = None
    else:
        result_dictionary[f'{property_name}_{first_child}'] = None
        result_dictionary[f'{property_name}_{second_child}'] = None


# Добавить обработку случаев с 0 полями
def append_to_array_vacancies(items):
    added_vacancy = []
    for index in range(0, len(items)):
        vacancy = {
            'id': items[index]['id'],
            'name': items[index]['name'],
            'url': items[index]['apply_alternate_url'],
            'employment_id': items[index]['employment']['id'],
            'employment_name': items[index]['employment']['name'],
        }

        write_properties(vacancy, items[index], 'salary', 'from', 'to')
        write_properties(vacancy, items[index], 'snippet', 'requirement', 'responsibility')
        write_properties(vacancy, items[index], 'experience', 'id', 'name')
        write_properties(vacancy, items[index], 'employment', 'id', 'name')
        write_properties(vacancy, items[index], 'employer', 'id', 'name')
        write_properties(vacancy, items[index], 'address', 'lat', 'lng')
        write_properties(vacancy, items[index], 'professional_roles', 'id', 'name')

        added_vacancy.append(vacancy)

    return added_vacancy


def get_vacancies(area_id, area_name):
    headers = {
        "Authorization": "Bearer " + TOKEN
    }

    result = []

    r = requests.get(f'https://api.hh.ru/vacancies?{AREA}={area_id}&per_page=100&page=0', headers=headers)

    print(f'area: {area_name}, id: {area_id}, status: {r.status_code}')

    if r.status_code == requests.codes.ok:
        json_data = r.json()

        print(f'founded: {json_data[FOUND]}')
        if 100 >= json_data[FOUND]:
            items = json_data[ITEMS]

            result += append_to_array_vacancies(items)

        else:
            items = json_data[ITEMS]

            result += append_to_array_vacancies(items)

            cycle_count = json_data['pages']
            print(f'cycle count {cycle_count}')

            for index in range(0, cycle_count - 1):
                r_cycle = requests.get(f'https://api.hh.ru/vacancies?{AREA}={area_id}&per_page=100&page={index + 1}',
                                       headers=headers)

                print(f'area: {area_name}, id: {area_id}, status: {r.status_code}')

                if r.status_code != requests.codes.ok:
                    continue

                json_cycle_data = r_cycle.json()

                items_cycle = json_cycle_data[ITEMS]

                result += append_to_array_vacancies(items_cycle)

        return result

    return result
