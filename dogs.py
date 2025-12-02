import requests
import json

yandex_token = input("Введите яндекс-токен: ").strip()
group_name = "FPY-140"

dog = input("Введите название породы на английском языке: ").strip().lower()
# https://dog.ceo/api/breed/hound/list


#  папка
headers = {'Authorization': yandex_token}
params = {'path': group_name}
response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                        params=params, headers=headers)



# количество собак
response = requests.get(f"https://dog.ceo/api/breed/{dog}/list")
# print(response.status_code)
if response.status_code != 200:
    print("Такой породы нет")
    exit()

all_dogs = response.json().get('message', [])
count_breeds = len(all_dogs)

if count_breeds == 0:
    response = requests.get(f"https://dog.ceo/api/breed/{dog}/images/random")
    if response.status_code == 200:
        link = response.json()['message']
        url_name = link.split('/')[-1]
        filename = f"{dog}_{url_name}"
        params = {'url': link,
                  'path': f'{group_name}/{filename}.jpg'
                  }
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                         headers=headers, params=params)
    #     with open(f'{filename}', 'wb') as f:
    #         f.write(requests.get(link).content)
        print("Получена ссылка на фотографию собачки")
    else:
        print("Не удалось получить ссылку на фотографию собачки")
    
else:
    for sub_breed in all_dogs:
        response = requests.get(f"https://dog.ceo/api/breed/{dog}/{sub_breed}/images/random")
        # print(response.status_code)
        if response.status_code == 200:
            link = response.json()['message']
            url_name = link.split('/')[-1]
            filename = f"{dog}_{url_name}"
            params = {
                'url': link,
                'path': f'{group_name}/{filename}.jpg'
                }
            response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                         headers=headers, params=params)
            print("Фотографии собачек сохранены на диск")        
        else:
            print("Не удалось сохранить фотографии на диск")

