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

def prepare_real_estate_churn_dataset():
    import pandas as pd
    import numpy as np
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    @task()
    def create_table() -> None:
        from sqlalchemy import MetaData, Table, Column, Integer, UniqueConstraint, inspect, Float, Boolean, BigInteger

        db_conn = PostgresHook("destination_db").get_sqlalchemy_engine().connect()
        metadata = MetaData()
        table = Table('real_estate_churn', metadata, 
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
            Column('studio', Boolean),
            Column('total_area', Float),
            Column('price', BigInteger),
            UniqueConstraint('id', name='unique_id_constraint')
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
        sql = f"""
                select f.id, 
                    f.building_id, 
                    b.build_year, 
                    b.building_type_int, 
                    b.latitude, 
                    b.longitude, 
                    b.ceiling_height, 
                    b.flats_count, 
                    b.floors_total, 
                    b.has_elevator,
                    f.floor,
                    f.is_apartment,
                    f.kitchen_area,
                    f.living_area,
                    f.rooms,
                    f.studio,
                    f.total_area,
                    f.price
                from flats f
                left join buildings b on f.building_id = b.id
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        """
        #### Transform task
        """
        return data

    @task()
    def load(data: pd.DataFrame):
        """
        #### Load task
        """
        hook = PostgresHook('destination_db')
        hook.insert_rows(
            table="real_estate_churn",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['id'],
            rows=data.values.tolist()
    )

    create_table() 
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)

prepare_real_estate_churn_dataset()