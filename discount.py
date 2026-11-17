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
    if not isinstance(product_id, int):
        print("Ошибка: product_id должен быть числом")
        return None
    if not isinstance(base_price, (int, float)):
        print("Ошибка: base_price должен быть числом")
        return None
    if base_price <= 0:
        print("Ошибка: цена должна быть > 0")
        return None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE oi.product_id = %s
              AND o.order_date >= CURRENT_DATE - INTERVAL '1 month';
        """, (product_id,))
        result = cursor.fetchone()
        orders_count = result[0]
        if orders_count == 0:
            return base_price * 0.75
        else:
            return base_price
    except psycopg2.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    result = calculate_price(1, 1000)
    print(f"Результат: {result}")

def calculate_price_esports_shop(item_id, base_price):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE oi.product_id = %s
              AND o.order_date >= CURRENT_DATE - INTERVAL '1 month';
        """, (item_id,))
        result = cursor.fetchone()
        orders_count = result[0]
        if orders_count == 0:
            return base_price * 0.75
        else:
            return base_price
    except psycopg2.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    result = calculate_price_esports_shop(1, 1490)
    print(f"Результат для товара 1: {result}")