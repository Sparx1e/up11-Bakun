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

def calculate_price(product_id, base_price):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.product_id = %s
              AND o.order_date >= CURRENT_DATE - INTERVAL '1 month';
        """, (product_id,))
        result = cursor.fetchone()
        orders_count = result[0]
    except psycopg2.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()