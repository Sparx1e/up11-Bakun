import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "esports_shop",
    "user": "postgres",
    "password": "123"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("Подключение работает")
    cursor.close()
    conn.close()
except psycopg2.Error as e:
    print(f"Ошибка БД: {e}")