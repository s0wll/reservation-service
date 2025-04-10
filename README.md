# reservation-service

ReservationServiceAPI - это REST API для бронирования столиков в ресторане. Сервис предоставляет эндпоинты для создания, просмотра и удаления бронирований, а также для управления столиками и временными слотами.

## Особенности
- Интеграция с базой данных для постоянного хранения
- Управление столами и бронированиями
- Разделение проекта на слои, с применением архитектурных паттернов
- Хорошо структурированные эндпоинты API для легкого доступа к ресурсам
- Тестирование для обеспечения надежности


## Установка

1. Клонируйте репозиторий, находясь в директории, куда хотите скачать проект:
```bash
git clone https://github.com/s0wll/reservation-service.git
```
2. Перейдите в директорию проекта:
```bash
cd reservation-service
```
3. В корне проекта создайте файл .env и установите в нем следующие значения:
```bash
MODE=LOCAL

DB_HOST=reservation_db
DB_PORT=5432
DB_USER=reservation_user
DB_PASS=reservation_pass
DB_NAME=reservation-service
```

## Запуск

Запустите Docker Compose с помощью следующей команды:
```bash
docker compose up --build
```

Для запуска приложения только с логами API, вместо команды выше выполните:
```bash
docker compose up -d --build
```
```bash
docker logs --follow reservation_back
```

Для соединения с БД, создайте новое подключение к PostgreSQL со следующими параметрами:
- Хост - localhost
- Порт - 6432
- Имя пользователя - reservation_user
- Пароль - reservation_pass

## Документация

API документация доступна по адресу: http://localhost/docs

## Тестирование

1. Для проведения тестирования, в корне проекта необходимо создать дополнительный файл .env-test и установить в нем следующие значения:
```bash
MODE=TEST

DB_HOST=localhost
DB_PORT=5432
DB_USER=(ваше имя пользователя postgres)
DB_PASS=(ваш пароль postgres)
DB_NAME=reservation-service-test
```

2. Далее создайте дополнительную базу данных в PostgreSQL (локальное соединение) и назовите ее "reservation-service-test".

3. Далее создайте и запустите виртуальное окружение с помощью команд (Я использовал в разработке версию Python 3.13.1):
```bash
python3 -m venv venv
```

Для MacOS/Linux:
```bash
source venv/bin/activate
```
Для Windows:
```bash
venv\Scripts\activate.bat
```
   
Не забудьте выбрать правильное venv в вашем редакторе кода (В случае с VSCode - это "Recommended").

4. Далее скачайте зависимости, выполнив команду:
```bash
pip install -r requirements.txt
```

5. После этого, для запуска тестирования, выполните следующую команду:
```bash
pytest -v -s
```

Если возникнут проблемы с переменными окружения, то выполните следующие команды, чтобы сбросить их значения:
```bash
unset MODE
```
```bash
unset DB_HOST
```
```bash
unset DB_PORT
```
```bash
unset DB_USER
```
```bash
unset DB_PASS
```
```bash
unset DB_NAME
```
