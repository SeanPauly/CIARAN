import pandas as pd
import numpy as np
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Load conversation data from CSV
file_path = '/Users/seanm/OneDrive/Projects/CIARAN/data/input/text/ab_conversation_data.csv'
conversation_data = pd.read_csv(file_path)

# Combine the conversation from both Person 1 and Person 2 into one column
conversation_data['Combined'] = conversation_data['Person 1'] + ' ' + conversation_data['Person 2']

# Prepare text for tokenization
text_data = conversation_data['Combined'].values.tolist()

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text_data)

total_words = len(tokenizer.word_index) + 1

# Generate input sequences for training
input_sequences = []
for line in text_data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

max_sequence_len = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
label = tf.keras.utils.to_categorical(label, num_classes=total_words)

# Model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(total_words, 100, input_length=max_sequence_len - 1),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150)),
    tf.keras.layers.Dense(total_words, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Model training
model.fit(predictors, label, epochs=100, verbose=1)
model.save_weights('model_weights.h5')

# Text generation function
def generate_text(seed_text, next_words, max_sequence_len):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted_probs = model.predict(token_list)[0]
        predicted = np.argmax(predicted_probs)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

# Loading model weights
model.load_weights('model_weights.h5')

# Generating text
generated_text = generate_text("Hello", 5, max_sequence_len)
print(generated_text)
