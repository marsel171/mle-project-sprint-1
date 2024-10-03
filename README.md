# Проект 1 спринта

 - Проект 1 спринта. 
 - Цель проекта — создать базовое решение для предсказания стоимости квартир Яндекс Недвижимости.

Имя бакета:
s3-student-mle-20240919-f8666628fb


## Этап 1. Сбор данных
Даг по выгрузке данных из исходного источника в таблицу real_estate_churn:
```
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/dags/churn.py
```
### Описание дага
С помощью Airflow собираем две таблицы в единый датасет с характеристиками квартир в персональной базе данных.
 - На этапе create_table создаем пустую таблицу real_estate_churn.
 - На этапе extract джойним 2 таблицы buildings и flats по ключу id-building_id.
 - На этапе transform пока ничего не предпринимаем.
 - На этапе load грузим в таблицу real_estate_churn.

### Ноутбук:
```
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/notebooks/select.ipynb
```


## Этап 2. Очистка данных
Даг по очистке данных из таблицы real_estate_churn в таблицу clean_real_estate_churn:
```
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/dags/clean_churn.py
```
### Описание дага
Анализируем данные на наличие наиболее распространённых проблем: дубликатов, пропусков и выбросов. 
 - На этапе create_table создаем пустую таблицу clean_real_estate_churn.
 - На этапе extract забираем все данные из таблицы real_estate_churn.
 - На этапе transform избавляемся от дублей, пропусков и выбросов.
 - На этапе load грузим в таблицу clean_real_estate_churn.

### Ноутбуки:
```
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/notebooks/dataset_data_analyze.ipynb
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/notebooks/dataset_preprocc.ipynb
/home/mle-user/mle_projects/mle-project-sprint-1/part1_airflow/notebooks/delete_table.ipynb
```


## Этап 3. Создание DVC-пайплайна обучения модели
Даг по обучению, оценке и сохранению модели, запуску DVC-пайплайна: 
```
/home/mle-user/mle_projects/mle-project-sprint-1/part2_dvc/
```

### Описание этапов DVC-пайплайна


### Ноутбуки:
```
/home/mle-user/mle_projects/mle-project-sprint-1/part2_dvc/notebooks/dataset_data_analyze.ipynb
```
путь до файлов с Python-кодом для этапов DVC-пайплайна;
путь до файлов с конфигурацией DVC-пайплайна dvc.yaml, params.yaml, dvc.lock.
