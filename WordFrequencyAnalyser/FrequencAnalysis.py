from nltk.tokenize import sent_tokenize, word_tokenize
import re

def main():
    text = "Hello Mr. Smith. how are you doing today. Whats the weather like? The sky is pinkish-blue. Whats the programming language? Python is awesome. What should I eat? You shouldnt eat cardboard."
    #wordList = re.split(r'[,]', text)
    wordList = (sent_tokenize(text))


    questionList = []
    answerList = []

    for i, val in enumerate(wordList):
        if(i % 2 == 0):
            questionList.append((re.split(r',', val)))
        else:
            answerList.append((re.split(r',', val)))


    wordDict = {}
    wordCount = 0

    for i in questionList:
        for j in i:
            wordList = (word_tokenize(j))
            wordCount = len(wordList)
        for j in answerList:



if __name__ == '__main__':
    main()