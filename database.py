import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            upload_date TEXT NOT NULL,
            annotation TEXT,
            file_size INTEGER,
            width INTEGER,
            height INTEGER,
            mean_red INTEGER,
            mean_green INTEGER,
            mean_blue INTEGER
        )
    ''')

    conn.commit()
    conn.close()
