import sqlite3
from duties import duties_data_rows


def setup_database(db_name='duties.db'):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS duties (
    id INTEGER PRIMARY KEY,
    Duty TEXT,
    Description TEXT
    )
    """)

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS saved_duties (
        id INTEGER PRIMARY KEY
    )
    """)

    cur.executemany("INSERT OR REPLACE INTO duties VALUES (?, ?, ?)", duties_data_rows)

    con.commit()
    con.close()
    print("Database seeded.")

if __name__ == "__main__":
    setup_database()