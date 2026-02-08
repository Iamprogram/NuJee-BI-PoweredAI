from datetime import date, timedelta
from random import randint
import sqlite3

from app.config import settings


def seed() -> None:
    conn = sqlite3.connect(settings.db_path)
    with conn:
        conn.execute("DROP TABLE IF EXISTS sales")
        conn.execute(
            """
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                region TEXT NOT NULL,
                product TEXT NOT NULL,
                amount REAL NOT NULL
            )
            """
        )

        base = date.today() - timedelta(days=59)
        for i in range(60):
            day = str(base + timedelta(days=i))
            for region in ["NA", "EU", "APAC"]:
                conn.execute(
                    "INSERT INTO sales (date, region, product, amount) VALUES (?, ?, ?, ?)",
                    (day, region, "core", float(1000 + randint(-150, 200) + i * 5)),
                )
    conn.close()


if __name__ == "__main__":
    seed()
    print("Seeded data/bi.db with sample sales data")
