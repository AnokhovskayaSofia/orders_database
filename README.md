# Тестовое задание
> :book: Это скрипт на языке Python 3, *который работает с GoogleSheet, создает базу PostgreSQL и отправляет сообщения в канал Telegram.*

### Author
Аноховская Софья
____
### Для запуска в режиме разработки
> *должен быть установлен и запyщен PostgreSQL*

> *должен быть создан файл с конфигурационнами парамертами .env*
- Создайте и активируйте виртуальное окружение
```bash
python -m venv venv
source venv/Scripts/activate
```
 - Загрузите все пакеты и зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```
- Запустите проект
```bash
python main.py
```
____
### Для запуска проекта в Docker
> *должен быть создан файл с конфигурационнами парамертами .env*
- Скачайте образ из DockerHub
```bash
docker pull anokhovskaya/anokhovskaya_kanalserv
``` 
- Нужно собрать контейнер и запустить его
```bash
docker-compose up -d --build
```
____
### Файл .env:
> файл должен быть создан локально в корне проекта

> файл должен содержать следующие заполненные поля
```bash
google_file_ID
sheet_file
table_name

telegram_token
channel_name

POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
```
