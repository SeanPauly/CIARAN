import csv

data = [
    ['Person 1', 'Person 2'],
    ['Hey, how are you?',  "Hey Alice! I'm doing great, thanks. How about you?"],
    ["I'm good too! Just working on a project. What about you?", 'Nice! I just finished reading a book.'],
    # Add more conversations as needed
]

file_path = '/Users/seanm/OneDrive/Projects/CIARAN/data/input/text/ab_conversation_data.csv'

with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Person1', 'Person2'])  # Writing the header
    csvwriter.writerows(data)  # Writing the data rows
