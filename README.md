# Развертывание проекта
``` python
pip3 install -r requirements.txt
cd config
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
# Создание супер пользователя
```
python3 manage.py createsuperuser
```


# Swagger и redoc:
http://127.0.0.1:8000/swagger
http://127.0.0.1:8000/redoc


# Авторизация
- К апи можно без токена обращаться пока что

# Работа с слушателями (listener)

***Создать слушателя***
1. [POST]Отправляешь запрос с email и username в body на `/api/v1/listener/'
2. В ответ получаешь данные пользователя. 
![image](https://user-images.githubusercontent.com/74203877/158422848-3637a401-3dd7-47b5-96ff-6716eb6772c1.png)

***Удалить слушателя***
- Доступно администратору и текущему пользователю
2. [DELETE]Отправляешь запрос с ID слушателя `/api/v1/listener/{id}/`.
3. Возвращает статус код.


# Работа с комнатами (Room)

***Создать комнату***
1. Отправляешь [POST] запрос на `http://127.0.0.1:8000/api/v1/room/` со следующими полями в Body:
`
          1. name - принимает любое значение кроме null
          2. creator - id создателя комнаты
          3. rules - принимает любое значение
          4. playlist_id - Принмает любое значение кроме null
          5. guests - строка с id пользователей, каждый id резделен через запятую и пробел ", "
          6. sync - строка с id sync, каждый id резделен через запятую и пробел ", "`
3. Возвращает все поля комнаты. 
![image](https://user-images.githubusercontent.com/74203877/158424907-00ba4293-8a21-4acd-a890-74d17a7a8d21.png)

***Остальные интерфейсы для комнаты***

1. Все остальные взаимодействия производятся с конкретной комнатой по её ID `http://127.0.0.1:8000/api/v1/room/{ID}/`
2. [GET] - вернут комнату
3. [PUT] - полностью обновляет объект, все поля обязательны.
4. [PATCH] - можно обновлять отдельные поля
5. [DELETE] - удаляет комнату


# Работа с sync

2. [POST] - http://127.0.0.1:8000/api/v1/sync/  Отправляешь id трека - строка и guests - айдишники пользователей.

