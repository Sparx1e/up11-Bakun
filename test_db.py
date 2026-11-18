from database import Database


def main():
    db = Database()

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