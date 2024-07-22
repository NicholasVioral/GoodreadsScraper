import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import time

def book_exists(title, author):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM books WHERE title = ? AND author = ?', (title, author))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_book_to_db(book):
    if book_exists(book['title'], book['author']):
        print(f"Book already exists in the database: {book['title']} by {book['author']}")
        return
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO books (title, author, rating, image_url, book_url, genre, ratings_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (book['title'], book['author'], book['rating'], book['image_url'], book['book_url'], book['genre'], book['ratings_count']))
    conn.commit()
    conn.close()

def search_book(title):
    search_url = f"https://www.goodreads.com/search?q={requests.utils.quote(title)}"
    print(f"Searching for book: {title}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    response = requests.get(search_url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        print(f"Failed to search for book: {title}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    book_link_tag = soup.find('a', class_='bookTitle')
    
    if not book_link_tag:
        print(f"Book link not found for: {title}")
        return None
    
    book_url = "https://www.goodreads.com" + book_link_tag['href']
    print(f"Found book URL: {book_url}")
    return scrape_book(book_url, book_url)

def scrape_book(url, book_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        print(f"Failed to retrieve book page: {url}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        title_tag = soup.find('h1', class_='Text__title1')
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        print(f"Parsed title: {title}")
        
        author_tag = soup.find('a', class_='ContributorLink')
        author = author_tag.get_text(strip=True) if author_tag else "No author found"
        print(f"Parsed author: {author}")

        rating_tag = soup.find('div', class_='RatingStatistics__rating')
        if rating_tag:
            rating = float(rating_tag.get_text(strip=True))
            print(f"Parsed rating: {rating}")
        else:
            rating = 0.0
            print("Rating tag not found")

        image_tag = soup.find('img', class_='ResponsiveImage')
        image_url = image_tag['src'] if image_tag else "https://dryofg8nmyqjw.cloudfront.net/images/no-cover.png"
        print(f"Parsed image URL: {image_url}")

        genre_section = soup.find('div', {'data-testid': 'genresList'})
        print(f"Genre section HTML: {genre_section}")

        genre_tags = genre_section.find_all('span', class_='Button__labelItem') if genre_section else []
        genres = [genre_tag.get_text(strip=True) for genre_tag in genre_tags if genre_tag.get_text(strip=True) != "...more"]
        genre = ', '.join(genres) if genres else "No genre found"
        print(f"Parsed genre: {genre}")

        ratings_count_tag = soup.find('span', {'data-testid': 'ratingsCount'})
        ratings_count_text = ratings_count_tag.get_text(strip=True) if ratings_count_tag else "0"
        ratings_count = int(re.sub(r'\D', '', ratings_count_text))  # Remove non-numeric characters
        print(f"Parsed ratings count: {ratings_count}")

        book = {
            'title': title,
            'author': author,
            'rating': rating,
            'image_url': image_url,
            'book_url': book_url,
            'genre': genre,
            'ratings_count': ratings_count
        }
        save_book_to_db(book)
        return book
    except (AttributeError, ValueError) as e:
        print(f"Error parsing book: {e}")
        return None

def scrape_books_from_file(file_path):
    books = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines:
        title = line.strip()
        if title:
            book_info = search_book(title)
            if book_info:
                books.append(book_info)
            time.sleep(2)  # Simulate delay to prevent overloading the server
    return books

# Example usage
if __name__ == '__main__':
    books = scrape_books_from_file('books.txt')
    sorted_books = sorted(books, key=lambda x: x['rating'], reverse=True)

    for book in sorted_books:
        print(f"{book['title']} - {book['author']} - Rating: {book['rating']} - Image URL: {book['image_url']} - Book URL: {book['book_url']} - Genre: {book['genre']} - Ratings Count: {book['ratings_count']}")
