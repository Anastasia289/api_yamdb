# API для проекта YaMDb

## Описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения, такие как «Книги», «Фильмы», «Музыка». Пользователи могут оставлять к произведениям текстовые отзывы и ставять произведениям оценки, из чего формируется рейтинг. 


## Установка и запуск:

Клонировать репозиторий:   
 https://github.com/Anastasia289/api_yamdb.git   
   
Перейти в него в командной строке:  
```cd api_yamdb```  

Cоздать виртуальное окружение:   
```python -m venv venv ```  
  
Активировать виртуальное окружение:   
```source venv/bin/activate```  
  
Установить зависимости из файла requirements.txt:  
```python -m pip install -r requirements.txt```
  

Выполнить миграции:   
```python manage.py makemigrations ```  
``` python manage.py migrate```  

Запустить проект:   
```python3 manage.py runserver  ```



## Подробная документация по работе API:
http://127.0.0.1:8000/redoc/

## Примеры запросов:

Получение информации о произведении:   
GET /api/v1/titles/{titles_id}/  
Пример ответа:  
```
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}
```
Получение категорий:   
GET /api/v1/categories/  
Пример ответа:  
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
Получение списка всех комментариев к отзыву  
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/  
Пример ответа:  

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```

## Технологии:

Python  
Django

## Авторы: 

Алексей Чижов - управление пользователями   
Анастасия Богданова - произведения, категории и жанры   
Егор Кабитов - отзывы, комментарии, рейтинг произведений

