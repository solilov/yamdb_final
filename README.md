### Workflow status
![yamdb_final workflow](https://github.com/solilov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## CI/CD for the project API YAMDB

### <a name="Описание_проекта">Описание</a>

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
В каждой категории есть произведения: книги, фильмы или музыка. Сами произведения в YaMDb не хранятся.
Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.
Читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

### <a name="Технолигии в проекте">Технолигии в проекте</a>

- **Python 3**,
- **Django REST Framework**, 
- **Git**, 
- **Simple JWT** ,
- **PostgreSQL**,
- **Docker**, 
- **Nginx**,
- **Gunicorn**

### <a name="Workflow">Workflow</a>

- **Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest**,

  **Дальнейшие шаги пройдут только если push был в ветку master**
  
- **Сборка и доставка докер-образов на Docker Hub**,
- **Автоматический деплой проекта на боевой сервер**,
- **Отправка уведомления в Telegram**

### <a name="Инструкции для развертывания проекта на сервере">Инструкции для развертывания проекта на сервере:</a>

#### <a name="Настройка сервера">Настройка сервера</a>
- Проверить статус nginx
```
sudo service nginx status
```
- Если nginx запущен-остановить
```
 sudo systemctl stop nginx

```
- Установить Docker и Docker-compose
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Проверить установку 
```
sudo  docker-compose --version
```
- Создать папку nginx/
```
mkdir nginx
```

#### <a name="Подготовка для заупска workflow">Подготовка для заупска workflow</a>
- Выполнить форк проекта в свой аккаунт github

- Клонировать репозиторий и перейти в него в командной строке:
```
https://github.com/solilov/yamdb_final.git
```
```
cd yamdb_final/
```

- Cоздать и активировать виртуальное окружение, обновить pip:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
python3 -m pip install --upgrade pip
```
- Локальный запуск автотестов
```
pytest
```

- Скопировать подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
```
```
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
- В репозитории добавить данные для переменных в secrets
```
DOCKER_PASSWORD
SSH_KEY
DOCKER_REPO
DOCKER_USERNAME
USER
HOST
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
POSTGRES_PASSWORD
POSTGRES_USER
TELEGRAM_TO
TELEGRAM_TOKEN
```
- Выполнить push в репозиторий для запуска workflow

#### <a name="После успешного деплоя выполнить на сервере">После успешного деплоя выполнить на сервере</a>
-  Собрать статические файлы:
```
  docker-compose exec web python manage.py collectstatic --no-input
```
- Применить миграции
```
  docker-compose exec web python manage.py migrate --noinput
```
- Создать суперпользователя
```
  docker-compose exec web python manage.py createsuperuser
```
- При необходимости наполнить базу тестовыми данными
```
 docker-compose exec web python manage.py loaddata fixtures.json
```

- Документация к проекту доступна по адресу http://178.154.252.235/redoc/
- Приложение будет доступно по адресу http://178.154.252.235

### <a name="Авторы">Автор</a>

Солилов Александр  https://github.com/solilov
Гришин Виталий  https://github.com/Mdk918
Жумабаев Аманжол 