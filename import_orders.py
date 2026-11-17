import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost", 
    port=5432, 
    database="esports_shop",
    user="postgres",
    password="123"
)
cur = conn.cursor()

df = pd.read_csv(r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Orders_import.csv", encoding="utf-8-sig")

cur.execute("SELECT id, name, production FROM products")
prod_map = {(n.strip(), p.strip()): i for i, n, p in cur.fetchall()}

cur.execute("SELECT id, name FROM variants")
var_map = {n.strip(): i for i, n in cur.fetchall()}


cur.execute("SELECT id, last_name, first_name, middle_name FROM users")
user_map = {}
for uid, ln, fn, mn in cur.fetchall():
    ln = ln.strip() if ln else ""
    fn = fn.strip() if fn else ""
    mn = mn.strip() if mn else ""
    user_map[(ln, fn, mn)] = uid

print(f"Загружено: товаров={len(prod_map)}, вариантов={len(var_map)}, пользователей={len(user_map)}")

orders_cnt = 0
items_cnt = 0

for order_num, group in df.groupby("Номер заказа"):
    first = group.iloc[0]
    
    full_name = str(first["ФИО"]).strip()
    parts = full_name.split()
    
    if len(parts) == 3:
        ln, fn, mn = parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        ln, fn, mn = parts[0], parts[1], ""
    else:
        print(f"ОШИБКА: неверный формат ФИО: '{full_name}'")
        continue
        
    uid = user_map.get((ln, fn, mn))
    if not uid:
        print(f"Нет пользователя в БД: '{ln}' '{fn}' '{mn}'")
        continue

    order_date = pd.to_datetime(first["Дата заказа"]).date()

    cur.execute(
        "INSERT INTO orders (user_id, order_date) VALUES (%s, %s) RETURNING id",
        (uid, order_date)
    )
    order_id = cur.fetchone()[0] # type: ignore
    orders_cnt += 1

    for _, row in group.iterrows():
        pid = prod_map.get((str(row["Наименование товара"]).strip(), str(row["Производство"]).strip()))
        vid = var_map.get(str(row["Вариант исполнения"]).strip())
        
        if not pid or not vid:
            print(f"  ПРОПУСК позиции: {row['Наименование товара']} / {row['Вариант исполнения']}")
            continue
            
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, variant_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            order_id, pid, vid,
            int(row["Количество"]),
            float(row["Цена за единицу"])
        ))
        items_cnt += 1

conn.commit()
print(f"\nУСПЕХ! Вставлено заказов: {orders_cnt}, позиций: {items_cnt}")
cur.close()
conn.close()