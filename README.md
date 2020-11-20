# Универсальный чат MetaProject
 
### Установка и настройка
* Настройка переменных сред, необходимо скопировать файл: `example.env` > `.env`
* Настроить файл `.env` под свои нужды
* Запустить командой `docker-compose up --build`
* Если у вас сервис с БД лежит в отдельном контейнере с закрытым внешним портом, то возникнет необходимость настроить networks между контейнерами. [Подробнее](https://docs.docker.com/compose/networking/`)
### Запуск тестов
* `docker-compose exec chat_socket python src/unittests.py`

# Документация к чату

### Подключение к сокету
Подключение к серверу с сертификатом `wss://ip:port` \
Подключение к серверу без сертификата `ws://ip:port`

### Навигация ###
* Получение истории сообщений [get_history](#get_history)
* Отправка сообщений [send_message](#send_message)
* Обработка ошибок [см. тут](#Errors)
* Детальная информация по API [см. тут](#Другое)

### get_history [<меню>](#Навигация)
#### Запрос
```json
{
    "chat_id": "1",
    "token": "b58f7d184743106a8a66028b7a28937c",
    "event_type": "get_history",
    "message": null
}
```
#### Ответ
```json
{
    "type": "success",
    "event_type": "get_history",
    "messages": [
        {
          "type": "file",
          "text": "Hello",
          "is_my": true,
          "username": "Ivan Petrov",
          "created_at": 1605874010,
          "file_url": "/static_media/media/doc.xml",
          "chat_id": "1",
          "avatar": "/static_media/media/ivan_petrov.img",
          "user_id": "2",
          "id": "4"
        },
        {
          "type": "image",
          "text": null,
          "is_my": true,
          "username": "Ivan Petrov",
          "created_at": 1605874010,
          "file_url": "/static_media/media/image.img",
          "chat_id": "1",
          "avatar": "/static_media/media/ivan_petrov.img",
          "user_id": "2",
          "id": "5"
        },
        {
          "type": "text",
          "text": "Hello Ivan",
          "is_my": true,
          "username": "Ivan Petrov",
          "created_at": 1605874010,
          "file_url": null,
          "chat_id": "1",
          "avatar": "/static_media/media/ivan_petrov.img",
          "user_id": "2",
          "id": "6"
        }
    ],
    "detail": null
}
```


### send_message [<меню>](#Навигация)
#### Запрос
```json
{
    "chat_id": "1",
    "token": "b58f7d184743106a8a66028b7a28937c",
    "event_type": "send_file",
    "message": {
      "type": "file",
      "text": "Hello",
      "file_url": "/static_media/media/doc.xml"
    }
}
```
#### Ответ
```json
{
    "type": "success",
    "event_type": "send_file",
    "messages": [
        {
          "type": "file",
          "text": "Hello",
          "username": "Ivan Petrov",
          "is_my": true,
          "created_at": 1605874010,
          "file_url": "/static_media/media/doc.xml",
          "chat_id": "1",
          "avatar": "/static_media/media/ivan_petrov.img",
          "user_id": "2",
          "id": "4"
        }
    ],
    "detail": "Success"
}
```

### Errors [<меню>](#Навигация)
#### Типы ошибок и статусов
* `success` - Все окей, запрос успешно отработал.
* `server_error` - Ошибка на стороне сервера.
* `event_not_found` - Событие не найдено. (event_type)
* `token_validation_error` - Токен пустой или недействительный.
* `chat_not_exists` - Чат в который пришло сообщение - не найден.
#### Пример ошибки
#### Запрос
```json
{
    "chat_id": "1",
    "token": "b58f7d184743106a8a66028b7a28937c",
    "event_type": "send_file_and_message",
    "message": {
      "type": "file",
      "text": "Hello",
      "file_url": "/static_media/media/doc.xml"
    }
}
```
#### Ответ
```json
{
    "type": "event_not_found",
    "event_type": "send_file_and_message",
    "messages": null,
    "detail": "Event send_file_and_message not found"
}
```

### Другое [<меню>](#Навигация)
#### Типы событий
* `get_history` - Получить историю сообщений по чату.
* `send_message` - Отправить сообщение без файлов.
* `send_file` - Отправить файл с сообщением или без.
#### Типы сообщений
* `text` - Сообщение без файлов.
* `image` - Отправить картинку с текстом или без.
* `file` - Отправить файл с сообщением или без.