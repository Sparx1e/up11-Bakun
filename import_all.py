import pandas as pd
import psycopg2

BASE = r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources"

conn = psycopg2.connect(
host="localhost",
port=5432,
database="esports",
user="postgres",
password="123"
)
cur = conn.cursor()

df_products = pd.read_csv(BASE + r"\Products_import.csv", encoding="utf-8-sig")
for cat in df_products["Категория"].dropna().unique():
    cur.execute(
        "INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (cat,)
    )

df_variants = pd.read_csv(BASE + r"\Variants_import.csv", encoding="utf-8-sig")
for v in df_variants["Вариант исполнения"].dropna().unique():
    cur.execute(
        "INSERT INTO variants (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (v,)
    )

df_users = pd.read_csv(BASE + r"\Users_import.csv", encoding="utf-8-sig")
for r in df_users["Роль"].dropna().unique():
    cur.execute(
        "INSERT INTO roles (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (r,)
    )
conn.commit()

cur.execute("SELECT name, category_id FROM categories")
cat_map = dict(cur.fetchall())

cur.execute("SELECT name, variant_id FROM variants")
var_map = dict(cur.fetchall())

cur.execute("SELECT name, role_id FROM roles")
role_map = dict(cur.fetchall())

for _, r in df_products.iterrows():
    image = r["Изображение"] if pd.notna(r["Изображение"]) else None
    cur.execute("""
        INSERT INTO products
            (category_id, subcategory, production, name, image, description, composition, base_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (name, production) DO UPDATE SET
            category_id = EXCLUDED.category_id,
            subcategory = EXCLUDED.subcategory,
            image = EXCLUDED.image,
            description = EXCLUDED.description,
            composition = EXCLUDED.composition,
            base_price = EXCLUDED.base_price
    """, (
        cat_map[r["Категория"]],
        r["Подкатегория"],
        r["Производство"],
        r["Наименование товара"],
        image,
        r["Описание"],
        r["Состав"],
        r["Цена"]
    ))
conn.commit()

df_stock = pd.read_csv(BASE + r"\Stock_Items_import.csv", encoding="utf-8-sig")

cur.execute("SELECT name, production, product_id FROM products")
prod_map = {(n, p): i for n, p, i in cur.fetchall()}

for _, r in df_stock.iterrows():
    pid = prod_map[(r["Наименование товара"], r["Производство"])]
    vid = var_map[r["Вариант исполнения"]]
    cur.execute("""
        INSERT INTO stock_items (product_id, variant_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id, variant_id) DO UPDATE SET
            quantity = EXCLUDED.quantity,
            price = EXCLUDED.price
    """, (
        pid,
        vid,
        int(r["Количество доступное для заказа"]),
        r["Цена варианта"]
    ))
conn.commit()

for _, r in df_users.iterrows():
    cur.execute("""
        INSERT INTO users (login, last_name, first_name, middle_name, role_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (login) DO UPDATE SET
            last_name = EXCLUDED.last_name,
            first_name = EXCLUDED.first_name,
            middle_name = EXCLUDED.middle_name,
            role_id = EXCLUDED.role_id
    """, (
        r["Логин"],
        r["Фамилия"],
        r["Имя"],
        r["Отчество"],
        role_map[r["Роль"]]
    ))
conn.commit()

cur.execute("SELECT last_name, first_name, middle_name, user_id FROM users")
user_map = {(l, f, m): i for l, f, m, i in cur.fetchall()}

df_orders = pd.read_csv(BASE + r"\Orders_import.csv", encoding="utf-8-sig")
df_orders["Дата заказа"] = pd.to_datetime(df_orders["Дата заказа"]).dt.date

orders_unique = df_orders[["Номер заказа", "Дата заказа", "ФИО"]].drop_duplicates()

for _, r in orders_unique.iterrows():
    fio = r["ФИО"].split()
    uid = user_map[(fio[0], fio[1], fio[2])]
    cur.execute("""
        INSERT INTO orders (order_number, user_id, order_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (order_number) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            order_date = EXCLUDED.order_date
    """, (
        int(r["Номер заказа"]),
        uid,
        r["Дата заказа"]
    ))
conn.commit()

cur.execute("SELECT order_number, order_id FROM orders")
order_map = dict(cur.fetchall())

cur.execute("""
    SELECT p.name, p.production, v.name, s.stock_item_id
    FROM stock_items s
    JOIN products p ON p.product_id = s.product_id
    JOIN variants v ON v.variant_id = s.variant_id
""")
stock_map = {(pn, prod, vn): sid for pn, prod, vn, sid in cur.fetchall()}

for _, r in df_orders.iterrows():
    oid = order_map[int(r["Номер заказа"])]
    sid = stock_map[(
        r["Наименование товара"],
        r["Производство"],
        r["Вариант исполнения"]
    )]
    cur.execute("""
        INSERT INTO order_items (order_id, stock_item_id, quantity, historical_price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (order_id, stock_item_id) DO UPDATE SET
            quantity = EXCLUDED.quantity,
            historical_price = EXCLUDED.historical_price
    """, (
        oid,
        sid,
        int(r["Количество"]),
        r["Цена за единицу"]
    ))

conn.commit()
cur.close()
conn.close()
print("Импорт завершён")