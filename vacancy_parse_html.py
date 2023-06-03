import bs4
import html5lib

# Распарсить информацию из всего html документа
def parse_html(document):
    soup = bs4.BeautifulSoup(document, 'html5lib')

    prof_area = 'null'
    prof_area_raw = soup.find('span', {'class': 'inplace', 'data-field': 'professionalArea'})
    if prof_area_raw:
        prof_area = prof_area_raw.text

    education = 'null'
    education_raw = soup.find('span', {'class': 'inplace', 'data-field': 'education'})
    if education_raw:
        education = education_raw.text

    experience = 'null'
    experience_raw = soup.find('span', {'class': 'inplace', 'data-field': 'experience'})
    if experience_raw:
        experience = experience_raw.text

    driver_license_category = 'null'
    driver_license_category_raw = soup.find('span', {'class': 'inplace', 'data-field': 'driverLicenseCategory'})
    if driver_license_category_raw:
        driver_license_category = driver_license_category_raw.text

    return {
        'professionalArea': prof_area.encode().decode().replace('\t', '').replace('\n', ''),
        'experience': experience.encode().decode().replace('\t', '').replace('\n', ''),
        'education': education.encode().decode().replace('\t', '').replace('\n', ''),
        'driver_license_category': driver_license_category.encode().decode().replace('\t', '').replace('\n', '')
    }
