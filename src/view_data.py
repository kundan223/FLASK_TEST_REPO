import sqlite3

conn = sqlite3.connect("fraud_detection.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM transactions").fetchall()

print("Stored Transactions:\n")
for row in rows:
    print(row)

conn.close()
