from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import threading

app = Flask(__name__)

def get_books_from_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT title, author, rating, image_url, book_url, genre, ratings_count FROM books ORDER BY rating DESC')
    books = [{'title': row[0], 'author': row[1], 'rating': row[2], 'image_url': row[3], 'book_url': row[4], 'genre': row[5], 'ratings_count': row[6]} for row in c.fetchall()]
    conn.close()
    return books

def scrape_books_task(file_path):
    from scraper import scrape_books_from_file
    scrape_books_from_file(file_path)

def clear_books_from_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    print("Handling request... Method:", request.method)
    if request.method == 'POST':
        print("POST request received. Scraping books...")
        # Start the scraping task in a new thread
        threading.Thread(target=scrape_books_task, args=('books.txt',)).start()
        return redirect(url_for('home'))
    
    books = get_books_from_db()
    print(f"Number of books retrieved: {len(books)}")
    return render_template('index.html', books=books)

@app.route('/clear', methods=['POST'])
def clear():
    print("Clearing all books from the database...")
    clear_books_from_db()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)