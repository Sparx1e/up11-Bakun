import psycopg2
from psycopg2 import pool


class Database:
    def __init__(self):
        self.connection_pool = None
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1, 5,
                host="localhost",
                port=5432,
                database="esports_shop",
                user="postgres",
                password="123"
            )
            print("Пул соединений создан: minconn=1, maxconn=5")
        except psycopg2.Error as e:
            print(f"Ошибка БД: {e}")
            self.connection_pool = None

    def get_connection(self):
        if self.connection_pool is None:
            return None
        try:
            return self.connection_pool.getconn()
        except psycopg2.Error as e:
            print(f"Ошибка получения соединения: {e}")
            return None

    def release_connection(self, conn):
        if self.connection_pool is not None and conn is not None:
            self.connection_pool.putconn(conn)

    def close_all(self):
        if self.connection_pool is not None:
            self.connection_pool.closeall()
            print("Пул соединений закрыт")

    def get_products(self):
        """Возвращает список товаров для темы «Мир киберспорта»."""
        conn = self.get_connection()
        if conn is None:
            return []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM products")
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Ошибка запроса: {e}")
            conn.rollback()
            return []
        finally:
            self.release_connection(conn)