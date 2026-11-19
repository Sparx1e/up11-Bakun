from database import Database


def main():
    print("Подключение к базе данных...")
    try:
        db = Database()
        print("Успешно подключено! Получаем товары...")
        
        products = db.get_products()
        
        print(f"\nВсего получено товаров: {len(products)}")
        
        print("\n--- Первые 3 товара для проверки ---")
        for product in products[:3]:
            print(product)
            
        print("\n--- Последний товар для проверки ---")
        if products:
            print(products[-1])
            
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")

    conn = db.get_connection()
    if conn is None:
        print("Не удалось получить соединение из пула")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM products")
            result = cur.fetchone()
            print(f"Количество товаров в БД: {result[0]}") # type: ignore
    except psycopg2.Error as e:
        print(f"Ошибка запроса: {e}")
        conn.rollback()
    finally:
        db.release_connection(conn)

    db.close_all()


if __name__ == "__main__":
    import psycopg2
    main()