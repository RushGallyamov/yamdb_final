# api_yambd
![Actions Status](https://github.com/RushGallyamov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Описание:

Этот проект нужен чтобы продвинуться в обучении на Яндекс.Практикуме и
попрактиковать навыки командой разработки.


## Установка:

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:losdmi/api_yamdb.git
```
```
cd api_yamdb
```

2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source venv/bin/activate
```

3. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

4. Выполнить миграции:
```
python3 api_yamdb/manage.py migrate
```

5. Запустить проект:
```
python3 api_yamdb/manage.py runserver
```


## management-команда для загрузки сущностей из csv в базу

Можно загрузить все сущности сразу:
```
python3 api_yamdb/manage.py load_entity all
```

Либо отдельно перечислять нужные сущности:
```
python3 api_yamdb/manage.py load_entity category title
```


## Примеры:

TODO добавить примеры вызовов апи

Больше примеров на странице http://127.0.0.1:8000/redoc/
