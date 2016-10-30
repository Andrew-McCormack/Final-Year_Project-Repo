from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import re

class NLP:

    def tokenize(input):
        input = input.lower()
        input = re.sub(r"[^\w\d'\s]+",'',input)

        #extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', "i'm", "we're", "they're", "you're"]
        #sentence_splitter = PunktSentenceTokenizer(extra_abbreviations)

        #sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = word_tokenize(input)

        return tokens