# trademark search

## Для запуска:
1. pip install -r requirements.txt
2. python main.py

## Примеры обращения к API

### Поиск по слову
**POST http://0.0.0.0:8080/api/v1/search/** <br>
**POST DATA TYPE: application/json** <br>
**POST DATA KEYS: query** <br>

#### Пример:
POST DATA: {"query": "Новый знак качества"} <br>
RESPONSE: <br>
```json
{
    "message": "OK",
    "total_found": 3,
    "word_percent_found": 1.0,
    "query_items": [
        {
            "id": "2002704756",
            "img": "https://tmsearch.onlinepatent.ru/images/120/12019518-371d-42a2-bb93-9cca6fdbd356.jpg",
            "index": "217924",
            "mktu": [
                5
            ],
            "name": "НОВЫЙ ЗНАК КАЧЕСТВА"
        },
        {
            "id": "96701575",
            "img": "https://tmsearch.onlinepatent.ru/images/1ab/1ab1ebbc-6d09-43c5-b9f0-082d4e6d8f0b.jpg",
            "index": "155019",
            "mktu": [
                6
            ],
            "name": "ЗНАК"
        },
        {
            "id": "2007715829",
            "img": "https://tmsearch.onlinepatent.ru/images/ba5/ba58cc71-9224-48d7-bdc5-d2504c631367.jpg",
            "index": "360710",
            "mktu": [
                35
            ],
            "name": "ЗНАК"
        }
      ]
}
```

### Поиск по слову с учетом МКТУ
**POST http://0.0.0.0:8080/api/v1/search/** <br>
**POST DATA TYPE: application/json** <br>
**POST DATA KEYS: query, mktu_array** <br>
**NOTE:** mktu_array - строка, числа через запятую

#### Пример:
POST DATA: {"query": "Новый знак качества", "mktu_array": "5,35"} <br>
RESPONSE: <br>
```json
{
    "message": "OK",
    "total_found": 2,
    "word_percent_found": 1.0,
    "query_items": [
        {
            "id": "2002704756",
            "img": "https://tmsearch.onlinepatent.ru/images/120/12019518-371d-42a2-bb93-9cca6fdbd356.jpg",
            "index": "217924",
            "mktu": [
                5
            ],
            "name": "НОВЫЙ ЗНАК КАЧЕСТВА"
        },
        {
            "id": "2007715829",
            "img": "https://tmsearch.onlinepatent.ru/images/ba5/ba58cc71-9224-48d7-bdc5-d2504c631367.jpg",
            "index": "360710",
            "mktu": [
                35
            ],
            "name": "ЗНАК"
        }
      ]
}
```

### Информация по индексу
**POST http://0.0.0.0:8080/api/v1/trademark/** <br>
**POST DATA TYPE: application/json** <br>
**POST DATA KEYS: index** <br>

#### Пример:
POST DATA: {"index": "217924"} <br>
RESPONSE: <br>
```json
{
    "item": {
        "index": 217924,
        "main_title": "Товарный знак № 217924",
        "subtitle": "Действует",
        "priority": "нет данных",
        "member": "Акционерное общество \"Нижегородский химико-фармацевтический завод\", 603105, г.Нижний Новгород, ул.Салганская, 7 (RU)",
        "address": "нет данных",
        "send_date": "20.02.2002",
        "register_date": "26.07.2002",
        "publish_date": "12.09.2002",
        "expired_date": "20.02.2032"
    },
    "message": "ok"
}
```