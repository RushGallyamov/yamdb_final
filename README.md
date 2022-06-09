# api_yambd
![Actions Status](https://github.com/RushGallyamov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
## Описание:

Командный проект. Yatube REST API с документацией к нему, отвечал за взаимодействие с пользователем, авторизацию, выдачу токенов, предоставление разрешений на взаимодействие с объектами БД.



## Установка:

1. Клонировать репозиторий:
```
git clone git@github.com:RushGallyamov/yamdb_final.git
```
2. Перейти в папку с файлом docker-compose.yaml:
```
cd yamdb_final/infra/
```

3. Собрать и запустить контейнер:
```
docker-compose up -d --build
```


4. Выполнить миграции, создать суперпользователя, собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

5. Админка доступна:
```
http://localhost/admin/
```

6. Документация API на странице http://localhost/redoc/
```
http://localhost/redoc/
```

Развернутый проект можно посмотреть на странице:
http://51.250.96.39/api/v1/


## management-команда для загрузки сущностей из csv в базу

Можно загрузить все сущности сразу:
```
docker-compose exec web python manage.py load_entity all
```

Либо отдельно перечислять нужные сущности:
```
docker-compose exec web python manage.py load_entity category title
```

С уважением,
Рашит Галлямов

Контакты:
rashitgalliamov@yandex.ru
https://github.com/RushGallyamov
