import AnalyseFiles
import os
import NLP

NUM_FILES = 350
wordFrequencyDistribution  = {}

def main():
    subtitleFilesDirectory = os.path.join('./SubFiles')

    for i in os.listdir(subtitleFilesDirectory):
        if(i.endswith('.srt')):
            AnalyseFiles.AnalyseFiles(subtitleFilesDirectory + '/' + i, wordFrequencyDistribution)

    print('Chatbot is active!')

def start():
    print('What\'s on your mind?')
    while(True):
        userInput = input()
        response = generateResponse(userInput)
        if(response == None):
            print("Wow, you got me, I don't have a response for that one!")
        else:
            print(response)

def generateResponse(userInput):
    inputTokens = NLP.NLP.tokenize(userInput)
    responseDistribution = {}

    for inputToken in inputTokens:
        print(inputToken)
        tokenResponses = wordFrequencyDistribution.get(inputToken.lower())

        if(tokenResponses != None):
            for response in tokenResponses:
                responseValue = responseDistribution.get(response.nextSubtitle)
                newValue = response.weight
                if(responseValue != None):
                    newValue = newValue + responseValue
                responseDistribution[response.nextSubtitle] = newValue

    bestResponse = None
    bestResponseValue = -1

    for key, value in responseDistribution.items():
        if(value != None):
            if(value >= bestResponseValue):
                print(key)
                print(value)
                bestResponseValue = value
                bestResponse = key

    return bestResponse

if __name__ == "__main__":
    main()
    start()