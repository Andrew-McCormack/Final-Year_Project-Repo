from nltk.tokenize import sent_tokenize, word_tokenize
import re

class NLP:

    def tokenize(input):
        input = input.lower()
        tokens = word_tokenize(input)

        return tokens