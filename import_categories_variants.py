import pandas as pd, psycopg2

conn = psycopg2.connect(
host="localhost", 
port=5432,
database="esports_shop", 
user="postgres", 
password="123")
cur = conn.cursor()

df = pd.read_csv(r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Products_import.csv", encoding="utf-8-sig")
for cat in df["Категория"].dropna().unique():
    cur.execute("INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (cat,))

dfv = pd.read_csv(r"C:\Users\funny\OneDrive\Desktop\practice\up-11-Bakun\21 World of eSports\Appendix 2 Resources\Variants_import.csv", encoding="utf-8-sig")
for v in dfv["Вариант исполнения"].dropna().unique():
    cur.execute("INSERT INTO variants (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (v,))

conn.commit(); cur.close(); conn.close()
print("Справочники импортированы")