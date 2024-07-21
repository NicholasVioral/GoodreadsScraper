import sqlite3

def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            rating REAL,
            image_url TEXT,
            book_url TEXT,
            genre TEXT,
            ratings_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_columns():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE books ADD COLUMN genre TEXT')
    except sqlite3.OperationalError:
        print("Column 'genre' already exists.")
    
    try:
        c.execute('ALTER TABLE books ADD COLUMN ratings_count INTEGER')
    except sqlite3.OperationalError:
        print("Column 'ratings_count' already exists.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_columns()


