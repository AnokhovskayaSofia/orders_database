import psycopg2
from config import *

class DB():
    def __init__(self):
        self.connection = None
        self.cur = None
        self.create()
        pass

    def create(self):
        """Создаем PostgreSQL БД.
        """
        try:
            if not self.connection:
                self.connect()

            self.cur.execute(
                    '''CREATE TABLE IF NOT EXISTS orders (
                        ID INTEGER PRIMARY KEY,
                        ORDER_ID INTEGER NOT NULL UNIQUE,
                        USD_COST REAL NOT NULL,
                        ORDER_DATE CHAR(10) NOT NULL,
                        RUB_COST REAL NOT NULL);'''
                )
            print('[INFO DB] PostgreSQL create')
        except Exception as ex:
            print('[INFO DB] Error while creating with PostgreSQL', ex)

    def close(self):
        """Закрываем PostgreSQL БД.
        """
        self.cur.close()
        self.connection.close()

        self.connection = None
        self.cur = None

    def connect(self):
        """Подключаемся к PostgreSQL БД.
        
        - Использует переменные из config файла
        """
        try:
            self.connection = psycopg2.connect(user=POSTGRES_USER,
                                            password=POSTGRES_PASSWORD,
                                            host=POSTGRES_HOST,
                                            port=POSTGRES_PORT,
                                            database=POSTGRES_DB)
            self.connection.autocommit = True
            self.cur = self.connection.cursor()
            print('[INFO DB] PostgreSQL connect')
        except Exception as ex:
            print('[INFO DB] Error while updating rub cost', ex)
    
    def update_rub_cost(self, usd: float):
        """Обновление цены в рублях при изменение курса доллара.
        Input : актуальный курс доллара
        """
        try:
            if not self.connection:
                self.connect()

            self.cur.execute(
                    f'''UPDATE {table_name}
                        SET rub_cost = usd_cost * {usd};'''
                )
        except Exception as ex:
            print('[INFO DB] Error while updating rub cost', ex)


    def update_db(self, values):
        """Записываем и обновляем данные в БД.
        Input : данные для записи в БД
        """
        try:
            if not self.connection:
                self.connect()
            self.cur.execute('TRUNCATE orders;')
            query = ''
            for val in values[1:]:
                query += f'''INSERT INTO {table_name} VALUES{int(val[0]), int(val[1]), float(val[2]), val[3], float(val[4])}
                            ON CONFLICT (order_id)
                            DO UPDATE SET id={int(val[0])}, order_id={int(val[1])}, usd_cost={float(val[2])}, rub_cost={float(val[4])},  order_date={val[3]};\n'''

            # self.cur.execute('TRUNCATE orders;')
            self.cur.execute(query)

        except Exception as ex:
            print('[INFO DB] Error while updating table PostgreSQL', ex)
    
    def getdate_db(self):
        """Получаем данные из БД.
        """
        try:
            if not self.connection:
                self.connect()
            query = f'''
                    SELECT * FROM {table_name};
                    '''

            self.cur.execute(query)
            return self.cur.fetchall()

        except Exception as ex:
            print('[INFO DB] Error while getting data from table PostgreSQL', ex)


