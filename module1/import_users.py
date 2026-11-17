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

df = pd.read_csv(r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Users_import.csv", encoding="utf-8-sig")

inserted = 0
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO users (last_name, first_name, middle_name, login, role)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (login) DO NOTHING
    """, (
        str(row["Фамилия"]).strip(),
        str(row["Имя"]).strip(),
        str(row["Отчество"]).strip(),
        str(row["Логин"]).strip(),
        str(row["Роль"]).strip()
    ))
    inserted += (cur.rowcount == 1)

conn.commit()
print(f"Пользователи импортированы: {inserted}")
cur.close()
conn.close()