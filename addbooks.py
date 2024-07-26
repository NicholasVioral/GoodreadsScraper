import sqlite3

def remove_unwanted_books_from_db(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM books
        WHERE ratings_count < 1000 OR LOWER(title) LIKE '%boxed set%'
    """)
    conn.commit()
    conn.close()

def read_titles_from_db(db_filename):
    titles = []
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title
        FROM books
        WHERE ratings_count >= 1000 AND LOWER(title) NOT LIKE '%boxed set%'
    """)
    rows = cursor.fetchall()
    for row in rows:
        titles.append(row[0])
    conn.close()
    return titles

def save_titles_to_file(titles, txt_filename):
    with open(txt_filename, 'a', encoding='utf-8') as txtfile:  # Open the file in append mode
        for title in titles:
            txtfile.write(f"{title}\n")

def remove_duplicates_from_file(txt_filename):
    with open(txt_filename, 'r', encoding='utf-8') as txtfile:
        lines = txtfile.readlines()
    unique_titles = list(dict.fromkeys(lines))  # Remove duplicates while maintaining order
    with open(txt_filename, 'w', encoding='utf-8') as txtfile:
        txtfile.writelines(unique_titles)

def main():
    db_filename = 'books.db'  # Replace with your SQLite database file path
    txt_filename = 'books.txt'  # Replace with your TXT file path

    remove_unwanted_books_from_db(db_filename)
    titles = read_titles_from_db(db_filename)
    save_titles_to_file(titles, txt_filename)
    remove_duplicates_from_file(txt_filename)
    print(f"{len(titles)} book titles have been processed and duplicates removed from {txt_filename}")

if __name__ == '__main__':
    main()
