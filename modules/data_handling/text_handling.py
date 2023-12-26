import nltk
import string

def tokenize_text(text):
    """
    Tokenize the input text.
    """
    tokens = nltk.word_tokenize(text)
    return tokens

def lowercase_tokens(tokens):
    """
    Convert tokens to lowercase.
    """
    lowercase_tokens = [token.lower() for token in tokens]
    return lowercase_tokens

def remove_punctuation(tokens):
    """
    Remove punctuation from tokens.
    """
    no_punctuation_tokens = [token for token in tokens if token not in string.punctuation]
    return no_punctuation_tokens
