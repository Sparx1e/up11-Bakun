import pandas as pd, psycopg2

conn = psycopg2.connect(
    host="localhost", 
    port=5432,
    database="esports_shop", 
    user="postgres", 
    password="123")
cur = conn.cursor()

df = pd.read_csv(r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Stock_Items_import.csv", encoding="utf-8-sig")

cur.execute("SELECT id, name, production FROM products")
prod_map = {(n, p): i for i, n, p in cur.fetchall()}

cur.execute("SELECT id, name FROM variants")
var_map = {n: i for i, n in cur.fetchall()}

ok = bad = 0
for _, row in df.iterrows():
    pid = prod_map.get((row["Наименование товара"], row["Производство"]))
    vid = var_map.get(row["Вариант исполнения"])
    if not pid or not vid:
        print("ПРОПУСК:", row["Наименование товара"], "/", row["Вариант исполнения"]); bad += 1; continue
    cur.execute("""
        INSERT INTO stock_items (product_id, variant_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id, variant_id)
        DO UPDATE SET quantity = EXCLUDED.quantity, price = EXCLUDED.price
    """, (pid, vid, int(row["Количество доступное для заказа"]), float(row["Цена варианта"])))
    ok += 1

conn.commit()
print(f"stock_items: вставлено/обновлено {ok}, пропущено {bad}")
cur.close(); conn.close()