import json
def decod_json():
    data = open('data.json', 'r', encoding="UTF-8")
    object_str = json.load(data)
    print(object_str[0])

