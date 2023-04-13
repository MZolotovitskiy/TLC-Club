import requests
import json
from data.services import Services

search_api_server = "https://search-maps.yandex.ru/v1/"
geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
static_map_server = "https://static-maps.yandex.ru/1.x/"

search_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
geocoder_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

# address_ll = ""

search_params = {
    "apikey": search_api_key,
    "text": "тойота сервис",
    "lang": "ru_RU",
    # "ll": address_ll,
    'spn': "0.552069,0.400552",
    "type": "biz"
}

geocoder_params = {
    "apikey": geocoder_api_key,
    "format": "json"
}

static_params = {
    "l": "map"
}


def check_response(response):
    if not response:
        print("Ошибка выполнения запроса:")
        print(search_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return ConnectionError
    else:
        return True


def town_coords(town):
    global address_ll
    geocoder_params["geocode"] = town
    response = requests.get(geocoder_request, params=geocoder_params)
    if check_response(response):
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        search_params['ll'] = ','.join(toponym["Point"]['pos'].split())


def search(town):
    print(town)
    town_coords(town)
    # print(search_params)
    response = requests.get(search_api_server, params=search_params)
    if check_response(response):
        return handler(response.json())


def handler(json_data):
    services_list = []
    for i in json_data['features']:
        temp = Services()
        temp.name = i['properties']['name']
        temp.description = i['properties']['description']
        try:
            temp.hours = i['properties']['CompanyMetaData']['Hours']['text']
        except KeyError:
            temp.hours = '-'
        try:
            temp.url = i['properties']['CompanyMetaData']['url']
        except KeyError:
            temp.url = '-'
        temp.phones = '\t'.join([k['formatted'] for k in i['properties']['CompanyMetaData']['Phones']])
        temp.coordinates = ','.join([str(k) for k in i['geometry']['coordinates']])
        temp.map = get_map(temp.coordinates)
        temp.make_map()
        services_list.append(temp)
    return services_list


# print(search('Москва'))

def get_map(coord):
    static_params['ll'] = coord
    static_params['z'] = "16"
    static_params['pt'] = coord + ',pm2dbl'
    response = requests.get(static_map_server, params=static_params)
    if check_response(response):
        return response.content

# pt=37.560483,55.781446,pm2dbl