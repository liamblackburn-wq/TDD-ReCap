import sqlite3
from duties import duties_data_rows


def setup_database():
    con = sqlite3.connect("duties.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duties (
    id INTEGER PRIMARY KEY,
    Duty TEXT,
    Description TEXT
    )
    """)

    cur.executemany("INSERT OR REPLACE INTO Duties VALUES (?, ?, ?)", duties_data_rows)

    con.commit()
    con.close()
    print("Database seeded.")

if __name__ == "__main__":
    setup_database()