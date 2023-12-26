import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape book information
def scrape_books(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data using CSS selectors
        books = soup.select('article.product_pod')

        # Creating a list to store the scraped data
        data = []

        for book in books:
            title = book.select_one('h3 a')['title']
            price = book.select_one('div p.price_color').get_text(strip=True)
            availability = book.select_one('div p.availability').get_text(strip=True)
            
            # Appending the data to the list
            data.append({
                'Title': title,
                'Price': price,
                'Availability': availability
            })

        return data
    else:
        print('Failed to retrieve the web page')
        return None

# Function to save data to a CSV file
def save_to_csv(data, filename='books.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Availability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Writing header
        writer.writeheader()

        # Writing data
        for row in data:
            writer.writerow(row)

# Main function
def main():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    num_pages = 3  # Change this value based on the number of pages you want to scrape

    all_data = []

    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        page_data = scrape_books(url)

        if page_data:
            all_data.extend(page_data)

    if all_data:
        save_to_csv(all_data)
        print(f'Successfully scraped data from {num_pages} pages and saved to "books.csv".')
    else:
        print('No data to save.')

if __name__ == "__main__":
    main()
