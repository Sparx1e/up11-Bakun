import psycopg2
from discount import DB_CONFIG

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "esports_shop",
    "user": "postgres",
    "password": "123"
}

try:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'products';
            """)
            columns = [row[0] for row in cursor.fetchall()]
            print("Столбцы в таблице products:", columns)
except psycopg2.Error as e:
    print(f"Ошибка БД: {e}")
