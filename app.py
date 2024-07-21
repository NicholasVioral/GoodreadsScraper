from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_books_from_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT title, author, rating, image_url, book_url, genre, ratings_count FROM books ORDER BY rating DESC')
    books = [{'title': row[0], 'author': row[1], 'rating': row[2], 'image_url': row[3], 'book_url': row[4], 'genre': row[5], 'ratings_count': row[6]} for row in c.fetchall()]
    conn.close()
    return books

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Handling request... Method:", request.method)
    if request.method == 'POST':
        print("POST request received. Scraping books...")
        from scraper import scrape_books_from_file  # Import here to avoid circular imports
        scrape_books_from_file('books.txt')
    
    books = get_books_from_db()
    print(f"Number of books retrieved: {len(books)}")
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)

