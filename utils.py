import re

def clean(text):
    return re.sub("\W+", " ", text)
    
def string_to_words(text):
    words = set(text.split(" "))
    words.discard("")
    return list(words)
    
def file_to_words(path):
    with open(path, "r") as p:
        text = clean(p.read())
    return string_to_words(text)
