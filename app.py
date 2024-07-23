from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import threading

app = Flask(__name__)

def get_books_from_db(genres=None, search_query=None, sort_by='rating'):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if genres:
        query = '''SELECT title, author, rating, image_url, book_url, genre, ratings_count 
                   FROM books 
                   WHERE ''' + ' AND '.join(['genre LIKE ?'] * len(genres)) + ' ORDER BY ' + sort_by + ' DESC'
        params = ['%' + genre + '%' for genre in genres]
    elif search_query:
        query = '''SELECT title, author, rating, image_url, book_url, genre, ratings_count 
                   FROM books 
                   WHERE title LIKE ? OR author LIKE ? 
                   ORDER BY ''' + sort_by + ' DESC'
        params = ['%' + search_query + '%', '%' + search_query + '%']
    else:
        query = '''SELECT title, author, rating, image_url, book_url, genre, ratings_count 
                   FROM books 
                   ORDER BY ''' + sort_by + ' DESC'
        params = []
    c.execute(query, params)
    books = [{'title': row[0], 'author': row[1], 'rating': row[2], 'image_url': row[3], 'book_url': row[4], 'genre': row[5], 'ratings_count': row[6]} for row in c.fetchall()]
    conn.close()
    return books

def get_all_genres():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT genre FROM books')
    genres = c.fetchall()
    conn.close()
    # Flatten the list and split genres by comma if they are stored as comma-separated strings
    unique_genres = set()
    for genre_tuple in genres:
        for genre in genre_tuple[0].split(','):
            unique_genres.add(genre.strip())
    return sorted(unique_genres)

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
    genres = get_all_genres()
    print(f"Number of books retrieved: {len(books)}")
    return render_template('index.html', books=books, genres=genres, selected_genres=[], selected_sort='rating')

@app.route('/clear', methods=['POST'])
def clear():
    print("Clearing all books from the database...")
    clear_books_from_db()
    return redirect(url_for('home'))

@app.route('/filter', methods=['GET'])
def filter_by_genre():
    genres = request.args.getlist('genre')
    books = get_books_from_db(genres)
    all_genres = get_all_genres()
    return render_template('index.html', books=books, genres=all_genres, selected_genres=genres, selected_sort='rating')

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    books = get_books_from_db(search_query=query)
    genres = get_all_genres()
    return render_template('index.html', books=books, genres=genres, selected_genres=[], selected_sort='rating')

@app.route('/sort', methods=['GET'])
def sort_books():
    sort_by = request.args.get('sort_by', 'rating')
    books = get_books_from_db(sort_by=sort_by)
    genres = get_all_genres()
    return render_template('index.html', books=books, genres=genres, selected_genres=[], selected_sort=sort_by)

if __name__ == '__main__':
    app.run(debug=True)
