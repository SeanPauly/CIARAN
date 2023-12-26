import json
import re
import time
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import shutil
import tensorflow as tf

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Define the path to the name_gender_data JSON file
json_file_path = "name_gender_data.json"

# Load existing name-gender data from the JSON file
try:
    with open(json_file_path, "r") as json_file:
        name_gender_data = json.load(json_file)
except FileNotFoundError:
    name_gender_data = {}

# Preprocess the dataset (e.g., convert names to lowercase)
def preprocess_dataset(data):
    for name, gender in data.items():
        data[name] = gender.lower()

# Function to predict gender based on a name using a machine learning model
def predict_gender_with_model(name):
    # Convert the name to lowercase for case-insensitive matching
    name = name.lower()

    # Check if the name exists in the dataset
    if name in name_gender_data:
        return name_gender_data[name]
    else:
        # Use a machine learning model to predict gender
        model = train_machine_learning_model(name_gender_data)
        predicted_gender = model.predict([name])[0]
        return predicted_gender

# Function to train a machine learning model
def train_machine_learning_model(data):
    # Split the dataset into names and corresponding genders
    names = list(data.keys())
    genders = list(data.values())

    # Create a pipeline with a CountVectorizer and Multinomial Naive Bayes classifier
    model = Pipeline([
        ('vectorizer', CountVectorizer(analyzer='char', ngram_range=(1, 2))),
        ('classifier', MultinomialNB())
    ])

    # Train the model on the dataset
    model.fit(names, genders)
    
    return model

# Function to train and test the name gender predictor
def train_predictor():
    # Input a name and predict gender
    user_name = input("Name: ")
    predicted_gender = predict_gender_with_model(user_name)

    if predicted_gender == "unknown":
        gender = input("Please specify gender (male/female/other): ")
        name_gender_data[user_name.lower()] = gender  # Append user-provided gender to the dataset
        with open(json_file_path, "w") as json_file:
            json.dump(name_gender_data, json_file, indent=4)  # Update JSON file
        print("You specified the gender as '{}' for the name '{}'.".format(gender, user_name))
    else:
        confirmation = input("Predicted gender for '{}' is {}. Is this correct? (yes/no): ".format(user_name, predicted_gender))
        if confirmation.lower() == "yes":
            print("Predictor is correct! Adding '{}' to the dataset.".format(user_name))
            name_gender_data[user_name.lower()] = predicted_gender
            with open(json_file_path, "w") as json_file:
                json.dump(name_gender_data, json_file, indent=4)  # Update JSON file
        else:
            gender = input("Please specify gender (male/female/other): ")
            name_gender_data[user_name.lower()] = gender  # Append user-provided gender to the dataset
            with open(json_file_path, "w") as json_file:
                json.dump(name_gender_data, json_file, indent=4)  # Update JSON file
            print("You specified the gender as '{}' for the name '{}'.".format(gender, user_name))

user_preferences_path = "settings.json"

try:
    with open(user_preferences_path, "r") as json_file:
        user_preferences = json.load(json_file)
except FileNotFoundError:
    user_preferences = {}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

def set_voice():
    if assname == "Kira":
        # Set the voice based on the value of "assname"
        engine.setProperty('voice', voices[1].id)
    elif assname == "Kieran":
        # Set the voice based on the value of "assname"
        engine.setProperty('voice', voices[0].id)    
    else: 
        engine.setProperty("voice", voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening !")

def setup():
    speak(f"I am Kieran, your Complex-Integral, Algorithmically-Reliable, Artificial-Network")
    speak("What should I call you")
    uname = takeCommand().lower()
    predicted_gender = predict_gender_with_model(uname)

    if predicted_gender == "male":
        greet = f"Welcome Mr. {uname}"

    elif predicted_gender == "female":
        greet = f"Welcome Ms. {uname}"

    else:
        greet = f"Welcome {uname}"

    speak(greet)
    engine.setProperty('voice', voices[0].id)    
    speak("Would you prefer me?... Kieran", )
    engine.setProperty('voice', voices[1].id)    
    speak("Or, Would you prefer me?... Kira")
    assname = takeCommand()
    user_preferences = {"voice": assname, "name": uname, "gender": predicted_gender}  # Add name and gender to preferences
    with open("settings.json", "w") as json_file:
            json.dump(user_preferences, json_file, indent=4)

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    response = f"The current time is {current_time}."
    speak(response)

import re

def listen_for_wake_word(command, wake_word="Kira"):
    while True:
        command = takeCommand().lower()  # Assuming takeCommand() retrieves user input or speech

        try:
            # Recognize the wake word
            if wake_word in command:
                print("Wake word detected! Program is awake.")
                break
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def parse_duration(command):
    # Use regular expressions to extract the duration in seconds
    pattern = r"sleep for (\d+) (second|seconds|minute|minutes|hour|hours|day|days|week|weeks|month|months|year|years)"
    match = re.search(pattern, command)
    
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        
        if unit == "second":
            return value
        elif unit == "seconds":
            return value
        elif unit == "minute":
            return value * 60
        elif unit == "minutes":
            return value * 60
        elif unit == "hour":
            return value * 3600
        elif unit == "hours":
            return value * 3600
        elif unit == "day":
            return value * 86400
        elif unit == "days":
            return value * 86400
        elif unit == "week":
            return value * 604800
        elif unit == "weeks":
            return value * 604800
        elif unit == "month":
            return value * 2628000  # Approximate value
        elif unit == "months":
            return value * 2628000  # Approximate value
        elif unit == "year":
            return value * 31536000  # Approximate value
        elif unit == "years":
            return value * 31536000  # Approximate value
    
    return None

# Example usage
wake_word_detected = listen_for_wake_word(wake_word="Kira")  # Change wake-word as needed

if wake_word_detected:
    command = "sleep for 5 seconds"  # Replace with your actual user input or speech
    duration = parse_duration(command)
    if duration is not None:
        print(f"Sleeping for {duration} seconds...")
        time.sleep(duration)
    else:
        print("Invalid sleep command.")


def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
     
    return query

if __name__ == '__main__':
    clear = lambda: os.system('cls')
     
    # This Function will clean any
    # command before execution of this python file
    clear()    
    # Access the "voice" value from the first dictionary in the list
    assname = user_preferences.get("voice", "")
    set_voice()
    wishMe()
    # Load user preferences and set the voice
    user_preferences_path = "settings.json"

    try:
        with open(user_preferences_path, "r") as json_file:
            user_preferences = json.load(json_file)
    except FileNotFoundError:
        user_preferences = {}
    
    if not user_preferences:  # Check if user_preferences is empty
        setup()  # Call setup() only if user_preferences is empty

    while True:
        # Inside the main loop:
        command = takeCommand().lower()
        if command:
            if "time" in command:
                tell_time()
            # SLEEP
            elif "sleep" in command:
                duration = parse_duration(command)
                if duration is not None:
                    print(f"Sleeping for {duration} seconds...")
                    time.sleep(duration)
                    print("Wake up!")
            elif "exit" in command:
                speak("Goodbye!")
                break