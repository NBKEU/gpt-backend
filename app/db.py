import sqlite3
from pathlib import Path
from .config import SQLITE_PATH

Path(".").mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_last4 TEXT,
    protocol TEXT,
    auth_code TEXT,
    amount REAL,
    payout_type TEXT,
    payout_network TEXT,
    payout_target TEXT,
    result_status TEXT,
    reference TEXT,
    created_at TEXT
);
""")

conn.commit()
