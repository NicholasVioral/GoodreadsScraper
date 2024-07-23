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
    
    # Check if 'genre' column exists
    c.execute("PRAGMA table_info(books)")
    columns = [col[1] for col in c.fetchall()]
    if 'genre' not in columns:
        c.execute('ALTER TABLE books ADD COLUMN genre TEXT')
    
    # Check if 'ratings_count' column exists
    if 'ratings_count' not in columns:
        c.execute('ALTER TABLE books ADD COLUMN ratings_count INTEGER')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    add_columns()
