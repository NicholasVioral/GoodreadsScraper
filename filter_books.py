import csv

# Define input and output file paths
csv_file_path = 'books.csv'
txt_file_path = 'books.txt'

# Function to read the CSV and filter books by number of ratings
def filter_books(csv_file_path, min_ratings=1000):
    titles = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['ratings_count']) > min_ratings:
                titles.append(row['title'])
    return titles

# Function to write the filtered titles to a text file
def write_titles_to_txt(titles, txt_file_path):
    with open(txt_file_path, mode='w', encoding='utf-8') as txtfile:
        for title in titles:
            txtfile.write(title + '\n')

# Main script
if __name__ == "__main__":
    filtered_titles = filter_books(csv_file_path)
    write_titles_to_txt(filtered_titles, txt_file_path)
    print(f"Filtered titles have been written to {txt_file_path}")
