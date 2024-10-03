# Проект 1 спринта

*Цель проекта — создать базовое решение для предсказания стоимости квартир Яндекс Недвижимости.*

Имя бакета:
`s3-student-mle-20240919-f8666628fb`


## Этап 1. Сбор данных
Даг по выгрузке данных из исходного источника в таблицу `real_estate_churn`:
```
part1_airflow/dags/churn.py
```

***Описание дага***

С помощью Airflow собираем две таблицы в единый датасет с характеристиками квартир в персональной базе данных.
 - На этапе `create_table` создаем пустую таблицу `real_estate_churn`.
 - На этапе `extract` джойним 2 таблицы `buildings` и `flats` по ключу `id - building_id`.
 - На этапе `transform` пока ничего не предпринимаем.
 - На этапе `load` грузим в таблицу `real_estate_churn`.

***Ноутбук***
```
part1_airflow/notebooks/select.ipynb
```

## Этап 2. Очистка данных
Даг по очистке данных из таблицы `real_estate_churn` в таблицу `clean_real_estate_churn`:
```
part1_airflow/dags/clean_churn.py
```

***Описание дага***

Анализируем данные на наличие наиболее распространённых проблем: дубликатов, пропусков и выбросов. 
 - На этапе `create_table` создаем пустую таблицу `clean_real_estate_churn`.
 - На этапе `extract` забираем все данные из таблицы `real_estate_churn`.
 - На этапе `transform` избавляемся от дублей, пропусков и выбросов.
 - На этапе `load` грузим в таблицу `clean_real_estate_churn`.

***Ноутбуки***
```
part1_airflow/notebooks/dataset_data_analyze.ipynb
part1_airflow/notebooks/dataset_preprocc.ipynb
part1_airflow/notebooks/delete_table.ipynb
```


## Этап 3. Создание DVC-пайплайна обучения модели
Запуск DVC-пайплайна по обучению, оценке и сохранению модели в облачном хранилище S3: 
```
dvc repro part2_dvc/dvc.yaml
```

***Описание этапов DVC-пайплайна***
Анализируем данные на наличие наиболее распространённых проблем: дубликатов, пропусков и выбросов. 
 - На этапе `get_data` подгружаем данные с таблицы `clean_real_estate_churn` и сохраняем в `initial_data.csv`.
 - На этапе `fit_model` обучаем базовую модель, выполнив необходимую предобработку данных.
 - На этапе `evaluate_model` оцениваем полученную модель по выбранной метрике.
 - С помощью `dvc push` сохраняем обученную модель в облачном хранилище S3.

***Пути до файлов с конфигурацией DVC-пайплайна***
```
part2_dvc/dvc.yaml
part2_dvc/params.yaml
part2_dvc/dvc.lock
```

***Пути до файлов с Python-кодом для этапов DVC-пайплайна***
```
part2_dvc/scripts/data.py
part2_dvc/scripts/fit.py
part2_dvc/scripts/evaluate.py
```

***Путь до обученной модели и тренировочных данных***
```
part2_dvc/models/fitted_model.pkl
part2_dvc/data/initial_data.csv
```
