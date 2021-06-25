Это мой первый проект на aiohttp, поэтому мне было бы очень приятно получить обратную связь. Я постарался сделать подобие MVC и настроить взаимодействие alembic, SQLAlchemy и aiohttp.

Не делал проверку доступа, так как в задании этого не было. По той же причине для полей валюты и страны не создавал отдельных таблиц, хотя по-хорошему надо это сделать.

Также не смог найти удобного сериалайзера и обработки форм в aiohttp, поэтому логика сделана вручную. Возможно просто плохо искал.

В логике приложения. POST запрос отвечает за создание, а PUT за изменение. 

Для создания таблиц в базе данных используются команды
```shell
alembic revision --autogenerate
alembic upgrade head
```

Для запуска
```shell
python3 main.py
```

Для тестов
```shell
pytest tests.py
```

## Описание API
### Лимиты
#### GET
Ответ  
```json
[
  {
    "id": 0,
    "country": "RUS",
    "cur": "EUR",
    "amount": 1000
  }
]
```
#### POST
Запрос  
```json
[
  {
    "country": "RUS",
    "cur": "EUR",
    "amount": 1000
  }
]
```
Удачный ответ  
```json
{
  "status": 200, 
  "text": "OK"
}
```
Неудачные ответы
```json
{
  "status": 701, 
  "text": "API error"
}
```
```json
{
  "status": 702, 
  "text": "Bad value of country or cur"
}
```
```json
{
  "status": 705, 
  "text": "Has object with params"
}
```
#### PUT
Запрос  
```json
[
  {
    "country": "RUS",
    "cur": "EUR",
    "amount": 2000
  }
]
```
Удачный ответ  
```json
{
  "status": 200, 
  "text": "OK"
}
```
Неудачные ответы
```json
{
  "status": 701, 
  "text": "API error"
}
```
```json
{
  "status": 706, 
  "text": "No object with params"
}
```
#### DELETE
Запрос
```json
[
  {
    "country": "RUS",
    "cur": "EUR"
  }
]
```
Удачный ответ  
```json
{
  "status": 200, 
  "text": "OK"
}
```
Неудачный ответ
```json
{
  "status": 701, 
  "text": "API error"
}
```  

### Трансферы
#### POST
Запрос
```json
[
  {
    "date": "25/06/21 08:30:00",
    "country": "RUS",
    "cur": "EUR",
    "amount": 1000
  }
]
```
Удачный ответ  
```json
{
  "status": 200, 
  "text": "OK"
}
```
Неудачные ответы
```json
{
  "status": 701, 
  "text": "API error"
}
```
```json
{
  "status": 702, 
  "text": "Bad value of country or cur"
}
```
```json
{
  "status": 707, 
  "text": "Summary transfers bigger then limits"
}
```