import requests
import pandas as pd
import numpy as np
import json
import time


headers = {
    "authority": "mpstats.io",
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "cookie": '',
    "origin": "https://mpstats.io",
    "user-agent": ''
}

payload = {
    "startRow": 0,
    "endRow": 5000,
    "sortModel": [
        {
            "sort": "desc",
            "colId": "revenue"
        }
    ]
}

# переменная с дефолтным названием категории и диапазоном выгружаемого периода
querystring = {"path":'Здоровье',"d1":'',"d2":''}

# функция принимает 4 аргумента
# mp - название маркетплейса: wb - wildberries, ozn - ozon
# end_row - предельное количество выгружаемых строк за 1 вызов
# start_row - минимальный порог количества выгружаемых строк, по дефолту значение 0
# аргумент params позволяет модифицировать переменную querystring
def parse_data(mp, end_row, start_row=0, **params):
    # создаем динамический url
    url = f"https://mpstats.io/api/{mp}/get/category" 
    
    # модифицируем переменную querystring
    category = params.get('category')
    date_1 = params.get('date_1')
    date_2 = params.get('date_2')
    
    querystring['path'] = category 
    querystring['d1'] = date_1
    querystring['d2'] = date_2  
    
    # дефолтные значения для минимального и макисмального количества строк
    startRow = 0
    endRow = 5000
    
    # пустой массив для последующего сохранения датафреймов
    li = []
    
    # рекурсия для инкрементального увеличения количества выгружаемых строк
    for i in range(start_row, end_row):
        # на первом шаге оставляем значения по умолчанию
        if i == 0:
            
            r = requests.request("POST", url, json=payload, headers=headers, params=querystring).text

            # сохраняю реквест в json
            jsn = json.loads(r)
            
            # создаю дполнительный ключ с датой, так как в изначальных выгружаемых данных его нет
            for product in jsn['data']:
                product['date'] = '2022-07-01'
            
            # на каждой итерации сохраняю продукт в массив  
            for i in jsn['data']:
                li.append(i)
        else:
            # во всех остальных шагах, делается плюс 5000 строк к каждому вызову
            start_row += 5000
            end_row += 5000
            
            # модифицируется переменная payload, чтобы переписать количество выгружаемых строк
            payload['startRow'] = startRow
            payload['endRow'] = endRow
                
            r = requests.request("POST", url, json=payload, headers=headers, params=querystring).text

            jsn = json.loads(r)
            
            for product in jsn['data']:
                product['date'] = '2022-07-01'
                
            for i in jsn['data']:
                li.append(i)
    
    # из полученного массива делаю датафрейм со всеми данными    
    df = pd.json_normalize(li)
    
    return df

# пример вызова функции
df = parse_data('wb', 5, category='Здоровье', date_1='2022-07-01', date_2='2022-07-31')

print(df)