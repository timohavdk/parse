import bs4
import json
import html5lib


# Распарсить информацию из json
def parse_json(document):
    soup = bs4.BeautifulSoup(document, 'html5lib')

    scripts_with_json = soup.find_all('script', {'type': 'application/ld+json'})

    script_with_json = scripts_with_json[1]

    json_data = str(script_with_json.string)
    json_clear = json.loads(json_data)

    city = 'null'
    vacancy = 'null'
    salary = 'null'
    employment = 'null'

    if 'title' in json_clear:
        vacancy = json_clear['title']

    if 'employmentType' in json_clear:
        employment = json_clear['employmentType']

    if 'jobLocation' in json_clear:
        city = json_clear['jobLocation']['address']['addressLocality']

    if 'baseSalary' in json_clear:
        base_salary = json_clear['baseSalary']
        if 'value' in base_salary:
            value = base_salary['value']
            if 'value' in value:
                salary = int(text_to_number(value['value']))
            elif 'minValue' in value and 'maxValue' in value:
                salary = int((text_to_number(value['minValue']) + text_to_number(value['maxValue'])) / 2)
            elif 'minValue' in value:
                salary = int((text_to_number(value['minValue'])))
            else:
                salary = int((text_to_number(value['maxValue'])))

    return {
        'vacancy': vacancy,
        'salary': salary,
        'city': city,
        'employment': employment
    }


# Приведение текста к числу
def text_to_number(text):
    parts = text.split('.')
    target_number = 0

    if ('' != parts[0]):
        target_number = int(parts[0])

    return target_number
