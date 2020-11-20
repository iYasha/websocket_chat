# Универсальный чат MetaProject
 
### Установка и настройка
* Настройка переменных сред, необходимо скопировать файл: `example.env` > `.env`
* Настроить файл `.env` под свои нужды
* Запустить командой `docker-compose up --build`
* Если у вас сервис с БД лежит в отдельном контейнере с закрытым внешним портом, то возникнет необходимость настроить networks между контейнерами. [Подробнее](https://docs.docker.com/compose/networking/`)
### Запуск тестов
* `docker-compose exec chat_socket python src/unittests.py`