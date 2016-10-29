import os
import itertools, collections
from operator import eq
import Subtitle
import NLP
import WordResponse

MAX_TIME_DIFFERENCE = 2000
def main():

    global currentSubtitle
    global nextSubtitle

    firstRun = True

    try:
        subFile = open(os.path.join('./SubFiles/The.Godfather.1972.1080p.BluRay.x264.DTS.Rus.Ukr.Eng.HDclub_eng.srt'))
    except Exception:
        return 0

    # Get rid of number of lines in file symbol
    subFile.readline()


    lineNumber = 0
    firstRun = True
    currentSubtitle = ''

    while (True):
        subNumber = subFile.readline()
        subNumber = subNumber.strip()

        if ((subNumber == '') or (subNumber.isspace())):
            break
        else:

            lineNumber += 1

            timeSub = subFile.readline()

            if(timeSub == None):
                raise ValueError('Error parsing time subtitle')

            subtitleString = ''
            s = None
            newSubtitleFound = False
            nextSubtitleText = ''
            while (True):
                s = subFile.readline()
                if((s == '') or (s.isspace())):
                    break
                else:
                    if ((s.strip().startswith('-')) and (len(subtitleString) > 0)):
                        newSubtitleFound = True
                        nextSubtitleText = s
                    else:
                        subtitleString += s + ' '


            startTime = int(parse(timeSub.split('-->')[0]))
            stopTime = int(parse(timeSub.split('-->')[1]))

            number = int(subNumber)

            nextSubtitle = Subtitle.Subtitle(number, startTime, stopTime, subtitleString)


            if(firstRun == True):
                firstRun = False
                currentSubtitle = nextSubtitle
            else:
                # Add back in later
                #addToFrequencyDistribution(frequencyDistribution)
                addToFrequencyDistributionEmpty()
                if(newSubtitleFound):
                    nextSubtitle = Subtitle.Subtitle(number, startTime, stopTime, nextSubtitleText)
                    # Add back in later
                    #addToFrequencyDistribution(frequencyDistribution)
                    addToFrequencyDistributionEmpty()

        #return frequencyDistribution

def isTimeOk():
    global MAX_TIME_DIFFERENCE
    global currentSubtitle
    global nextSubtitle
    nextStartTime = nextSubtitle.startTime
    currEndTime = currentSubtitle.stopTime
    diff = nextStartTime - currEndTime
    return diff < MAX_TIME_DIFFERENCE

def subtitlesAreOk():
    global currentSubtitle
    global nextSubtitle

    nextSub = nextSubtitle.subtitleString

    if(currentSubtitle == None):
        return False
    elif(nextSub == None):
        return False
    elif(eq(nextSub.strip(), '')):
        return False
    elif(nextSub.strip().startswith('[') and nextSub.strip().endswith(']')):
        return False

    return True


def parse(input):
    split = []
    split = (input.split(':'))

    hours = int(split[0].strip())
    minutes = int(split[1].strip())
    seconds = int(split[2].split(',')[0].strip())
    millies = int(split[2].strip(',')[1].strip())

    return hours * 60 * 60 * 1000 + minutes * 60 * 1000 + seconds * 1000 + millies;


def addToFrequencyDistributionEmpty():
    global currentSubtitle
    global nextSubtitle

    if(isTimeOk()):
        if(subtitlesAreOk()):
            addToFrequencyDistributionNoFreq(currentSubtitle.subtitleString, nextSubtitle.subtitleString)
            currentSubtitle = nextSubtitle
            nextSubtitle = None
        else:
            currentSubtitle = nextSubtitle
        nextSubtitle = None

def addToFrequencyDistribution(frequencyDistribution):
    global currentSubtitle
    global nextSubtitle

    if(isTimeOk()):
        if(subtitlesAreOk()):
            addToFrequencyDistribution(frequencyDistribution, currentSubtitle.subtitleString, nextSubtitle.subtitleString)
            currentSubtitle = nextSubtitle
            nextSubtitle = None
        else:
            currentSubtitle = nextSubtitle
        nextSubtitle = None


def addToFrequencyDistributionNoFreq(currSubtitleText, nextSubtitleText):
    tokens = []
    tokens = NLP.NLP.tokenize(currSubtitleText)

    size = len(tokens)
    wordResponse = WordResponse.WordResponse(nextSubtitleText, 1.0 / size)

    responses = []
    for token in tokens:
        print(token)
        #responses = set(WordResponse)
        responses.append(wordResponse)


def addToFrequencyDistribution(frequencyDistribution, currSubtitleText, nextSubtitleText):
    tokens = []
    tokens = NLP.NLP.tokenize(currSubtitleText)

    size = len(tokens)
    wordResponse = WordResponse.WordResponse(nextSubtitleText, 1.0 / size)

    for token in tokens:
        responses = frequencyDistribution.get(token)
        if(responses == None):
            responses = set(WordResponse)

        responses.add(wordResponse)
        frequencyDistribution.put(token, responses)


if __name__ == '__main__':
    main()