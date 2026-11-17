import pandas as pd
import psycopg2

CSV_PATH = r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Products_import.csv"

conn = psycopg2.connect(
host="localhost",
    port=5432,
    database="esports_shop",
    user="postgres",
    password="123"
)

conn.autocommit = False
cur = conn.cursor()

try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    cur.execute("SELECT name, id FROM categories")
    cat_map = dict(cur.fetchall())

    missing = set(df["Категория"].unique()) - set(cat_map)
    if missing:
        raise ValueError(f"В таблице categories нет категорий: {missing}")

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        image = None if pd.isna(row["Изображение"]) else str(row["Изображение"])

        cur.execute(
            """
            INSERT INTO products
                (category_id, subcategory, image, name, production,
                 description, composition, base_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name, production) DO NOTHING
            """,
            (
                cat_map[row["Категория"]],
                str(row["Подкатегория"]),
                image,
                str(row["Наименование товара"]),
                str(row["Производство"]),
                str(row["Описание"]),
                str(row["Состав"]),
                float(row["Цена"])
            )
        )

        if cur.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    conn.commit()
    print(f"Импорт завершён. Вставлено: {inserted}, пропущено: {skipped}")

except Exception as e:
    conn.rollback()
    print("Ошибка импорта:", e)
    raise

finally:
    cur.close()
    conn.close()