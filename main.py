# main.py
# Import necessary modules/functions/classes
from modules.data_handling.text_handling import load_text_data, process_text
from modules.natural_language_processing.nlp_processing import analyze_text
from modules.user_interaction.user_interface import start_user_interface
import os

def main():
    data_directory = "/Users/seanm/OneDrive/Projects/CIARAN/data/input/text/" 
     # Replace with your data directory path
    analyzed_texts = []  # Initialize a list to store analyzed results

    for file_name in os.listdir(data_directory):
        if file_name.endswith('.csv'):  # Filter for CSV files (adjust the condition as needed)
            file_path = os.path.join(data_directory, file_name)
            text_data = load_text_data(file_path)

            if text_data is not None:
                # Inside the loop after loading text_data
                print(text_data.columns)
                # Assuming 'text' is the column containing text data
                # Analyze each text entry individually
            else:
                print(f"Failed to load text data from {file_name}")

    # Start user interface with all analyzed texts
    start_user_interface(analyzed_texts)

if __name__ == "__main__":
    main()