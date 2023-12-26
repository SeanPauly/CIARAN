from modules.data_handling.text_handling import tokenize_text, lowercase_tokens, remove_punctuation
import os


# main.py will run the user interface
# 
#

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def main():
    # File path for text data
    file_path = 'data/input/text/text_data.txt'
    
    # Read text from file
    if os.path.exists(file_path):
        text = read_text_from_file(file_path)
        
        # Tokenize text
        tokens = tokenize_text(text)
        print("Tokens:", tokens)
        
        # Lowercase tokens
        lowercase = lowercase_tokens(tokens)
        print("Lowercased tokens:", lowercase)
        
        # Remove punctuation
        no_punctuation = remove_punctuation(lowercase)
        print("Tokens without punctuation:", no_punctuation)
    else:
        print(f"File '{file_path}' not found.")

if __name__ == "__main__":
    main()
