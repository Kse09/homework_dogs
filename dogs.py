import requests
import json
import time
from tqdm import tqdm

dog = input("Введите название породы на английском языке: ").strip().lower()
yandex_token = input("Введите яндекс-токен: ").strip()
group_name = "FPY-140"

headers = {'Authorization': yandex_token}
params = {'path': group_name}
response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                        params=params, headers=headers)


response = requests.get(f"https://dog.ceo/api/breed/{dog}/list")
if response.status_code != 200:
    print("Такой породы нет")
    exit()
all_dogs = response.json().get('message', [])
count_breeds = len(all_dogs)

if count_breeds == 0:
    print("У выбранной Вами породы только один подвид")
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
        print("Подождите, фотографии загружаются")
        time.sleep(1)
        with tqdm(total=100) as pbar:
            for i in range(10):
                time.sleep(0.1)
                pbar.update(10)
        print("Фотография загружена на диск")
        time.sleep(3)
        params = {
            'path': f'{group_name}/{filename}.jpg',
            'fields': 'name,path,size' 
            }
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                           headers=headers, params=params)
    
        file_info = response.json()
        json_filename = f"{filename}_info.json"
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(file_info, json_file, ensure_ascii=False, indent=2)
        print("Информация о фотографии сохранена в json файле")
    else:
        print("Не получилось сохранить фотографию")


else:
    for sub_breed in all_dogs:
        print(f'У выбраннй Вами породы {count_breeds} подвид(ов)')
        response = requests.get(f"https://dog.ceo/api/breed/{dog}/{sub_breed}/images/random")
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
            print("Подождите, фотография загружается")
            time.sleep(1)
            with tqdm(total=100) as pbar:
                for i in range(10):
                    time.sleep(0.1)
                    pbar.update(10)
            print("Фотография собачки загружена на диск")
        time.sleep(3)
        params = {
            'path': f'{group_name}/{filename}.jpg',
            'fields': 'name,path,size' 
            }
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                           headers=headers, params=params)
        file_info = response.json()
        json_filename = f"{filename}_info.json"
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(file_info, json_file, ensure_ascii=False, indent=2)   
        print("Информация о фотографии сохранена в json файл") 

