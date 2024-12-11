# Это приложение парсит данные из access логов веб-сервера Apache и сохраняет их в базе данных PostgreSQL. Также предоставляет API для получения данных.

## Установка

# 1. Установите python 3.11 ( у меня на версии выше не запускался но при желании можете попробовать на версии выше)
# 2. Установите PostgreSQL
# 3. Установите зависимости
# pip install requirements.txt

# Создайте базу данных, после чего выполните скрипт чтобы создания таблицу

CREATE TABLE apache_logs (
       id SERIAL PRIMARY KEY,
       ip VARCHAR(15),
       date TIMESTAMP,
       method VARCHAR(10),
       path TEXT,
       http_version VARCHAR(10),
       status_code INTEGER,
       size INTEGER
   );

# Далее заполните данные для подключения к базе данных в файл конфигурации (config.ini)


# В папке logs непосредственно хранятся логи

## log_aggregator
# Непосредственно сам агрегатор логов, если вы изменили место хранение логов, то изменить нужно будет и в файле

## API.py
# для запуска АПИ используйте API.py
# Когда сервер активен запросы отправляются следующим образом
# http://127.0.0.1:5000/api/data?start=YYYY-MM-DD&end=YYYY-MM-DD&ip=IP_ADDRESS
# Поля запроса:
# start: Начальная дата в формате YYYY-MM-DD.
# end: Конечная дата в формате YYYY-MM-DD.
# ip: IP-адрес, по которому нужно фильтровать данные.
# Пример запроса:
# Если вы хотите получить данные с 1 января 2023 года по 31 декабря 2023 года для IP-адреса 192.168.1.1, примите следующее URL:
# http://127.0.0.1:5000/api/data?start=2023-01-01&end=2023-12-31&ip=192.168.1.1


## views.py 
# при использовании предложит вам найти нужные логи через консоль