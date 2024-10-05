import pendulum
from airflow.decorators import dag, task
from messages import send_telegram_success_message, send_telegram_failure_message

@dag(
    schedule='@once',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ETL", "project", "sprint 1"],
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message
)

def clean_real_estate_churn_dataset():
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    @task()
    def create_table() -> None:
        from sqlalchemy import MetaData, Table, Column, Integer, UniqueConstraint, inspect, Float, Boolean, BigInteger

        db_conn = PostgresHook("destination_db").get_sqlalchemy_engine().connect()
        metadata = MetaData()
        table = Table('clean_real_estate_churn', metadata, 
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('building_id', Integer),
            Column('build_year', Integer),
            Column('building_type_int', Integer),
            Column('latitude', Float),
            Column('longitude', Float),
            Column('ceiling_height', Float),
            Column('flats_count', Integer),
            Column('floors_total', Integer),
            Column('has_elevator', Boolean),
            Column('floor', Integer),
            Column('kitchen_area', Float),
            Column('living_area', Float),
            Column('rooms', Integer),
            Column('is_apartment', Boolean),
            Column('total_area', Float),
            Column('price', BigInteger),
            UniqueConstraint('id', name='unique_clean_id_constraint')
            )
        if not inspect(db_conn).has_table(table.name): 
            metadata.create_all(db_conn) 

    @task()
    def extract(**kwargs):
        """
        #### Extract task
        """
        hook = PostgresHook('destination_db')
        conn = hook.get_conn()
        sql = f"select * from real_estate_churn"
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        """
        #### Transform task
        """

        # Очистка данных от дубликатов, лишних фичей и артефактные price
        def remove_duplicates(data):
            feature_cols = data.columns.drop('id').tolist()

            # Отлично, дубли очищены! Возможно стоит оставлять один экземпляр (например, установить keep=first)
            is_duplicated_features = data.duplicated(subset=feature_cols, keep="first")
            # is_duplicated_features = data.duplicated(subset=feature_cols, keep=False)
            
            data = data[~is_duplicated_features].reset_index(drop=True)

            # удаляем колонку studio (т.к. в выборке всегда одно значение = 0)
            data = data.drop(columns=['studio']).reset_index(drop=True)

            # удаляем объекты с price меньше 1,000 и больше 1,000,000,000 (т.к. в выборке таких значений очень мало)
            data = data[data["price"] >= 1e+03 ].reset_index(drop=True)
            data = data[data["price"] < 1e+09].reset_index(drop=True)

            return data
        
        # # encoding bool features -> перенес на этап preprocessor в dvc-пайплайне
        # def bool_to_bincat(data):
        #     feature_cols = data.columns.drop('id').tolist()
        #     bool_cols = data[feature_cols].select_dtypes(['bool']).columns
        #     data[bool_cols] = data[bool_cols]*1
        #     return data

        # Заполнение пропусков
        def fill_missing_values(data):
            cols_with_nans = data.isnull().sum()
            cols_with_nans = cols_with_nans[cols_with_nans > 0].index
            for col in cols_with_nans:
                if data[col].dtype in [float, int]:
                    fill_value = data[col].mean()
                data[col] = data[col].fillna(fill_value)
            return data
        
        # Отсев выбросов по методу IQR (Interquantile Range)
        def remove_outliers(data):
            num_cols = data.select_dtypes(['float']).columns
            threshold = 1.5
            potential_outliers = pd.DataFrame()

            for col in num_cols:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                margin = threshold*IQR
                lower = Q1 - margin
                upper = Q3 + margin
                potential_outliers[col] = ~data[col].between(lower, upper)

            outliers = potential_outliers.any(axis=1)
            return data[~outliers]
        
        data = remove_duplicates(data)
        # data = bool_to_bincat(data)
        data = fill_missing_values(data)
        data = remove_outliers(data)

        return data

    @task()
    def load(data: pd.DataFrame):
        """
        #### Load task
        """
        hook = PostgresHook('destination_db')
        hook.insert_rows(
            table="clean_real_estate_churn",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['id'],
            rows=data.values.tolist()
    )

    create_table() 
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)

clean_real_estate_churn_dataset()