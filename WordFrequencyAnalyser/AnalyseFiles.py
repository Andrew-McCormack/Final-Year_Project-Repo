import os
import itertools, collections
from operator import eq
import Subtitle
import NLP
import WordResponse

class AnalyseFiles:

    currentSubtitle = None
    nextSubtitle = None

    def __init__(self, subtitleFile, wordFrequencyDistribution):
        self.analyse(subtitleFile, wordFrequencyDistribution)

    def analyse(self, subtitleFile, wordFrequencyDistribution):
        global currentSubtitle
        global nextSubtitle

        firstRun = True
        try:
            subFile = open(subtitleFile)
        except Exception:
            return 0

        # Get rid of number of lines in file symbol
        subFile.readline()


        lineNumber = 0
        firstRun = True

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

                startTime = int(self.parse(timeSub.split('-->')[0]))
                stopTime = int(self.parse(timeSub.split('-->')[1]))

                #print(startTime)
                #print(stopTime)

                number = int(subNumber)

                nextSubtitle = Subtitle.Subtitle(number, startTime, stopTime, subtitleString)


                if(firstRun == True):
                    firstRun = False
                    currentSubtitle = nextSubtitle
                else:
                    self.addToFrequencyDistributionWithFreq(wordFrequencyDistribution)
                    #self.addToFrequencyDistributionEmpty()
                    if(newSubtitleFound == True):
                        nextSubtitle = Subtitle.Subtitle(number, startTime, stopTime, nextSubtitleText)
                        self.addToFrequencyDistributionWithFreq(wordFrequencyDistribution)
                        #self.addToFrequencyDistributionEmpty()

            #return frequencyDistribution

    def isTimeOk(self):
        MAX_TIME_DIFFERENCE = 2000

        #print('Current sub is: ' + currentSubtitle.subtitleString)
        #print('Next sub is: ' + nextSubtitle.subtitleString)

        global currentSubtitle
        global nextSubtitle
        nextStartTime = nextSubtitle.startTime
        #print(nextStartTime)
        currEndTime = currentSubtitle.stopTime
        #print(currEndTime)
        diff = nextStartTime - currEndTime

        #print('Result is: ' + str((diff < MAX_TIME_DIFFERENCE)).lower())

        if(diff < MAX_TIME_DIFFERENCE):
            return True

        return False

    def subtitlesAreOk(self):
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

        #print('Returning true')
        return True


    def parse(self, input):
        split = []
        split = (input.split(':'))

        hours = int(split[0].strip())
        minutes = int(split[1].strip())

        secondsMillies = split[2].split(','.strip())

        seconds = int(secondsMillies[0])
        millies = int(secondsMillies[1])

        return hours * 60 * 60 * 1000 + minutes * 60 * 1000 + seconds * 1000 + millies;


    def addToFrequencyDistributionEmpty(self):
        global currentSubtitle
        global nextSubtitle

        if(self.isTimeOk()):
            if(self.subtitlesAreOk()):
                self.addToFrequencyDistributionNoFreq(currentSubtitle.subtitleString, nextSubtitle.subtitleString)
                currentSubtitle = nextSubtitle
                nextSubtitle = None
            else:
                currentSubtitle = nextSubtitle
            nextSubtitle = None

    def addToFrequencyDistributionWithFreq(self, frequencyDistribution):
        global currentSubtitle
        global nextSubtitle

        if(self.isTimeOk()):
            if(self.subtitlesAreOk()):
                self.addToFrequencyDistribution(frequencyDistribution, currentSubtitle.subtitleString, nextSubtitle.subtitleString)
                currentSubtitle = nextSubtitle
                nextSubtitle = None
        else:
            currentSubtitle = nextSubtitle

        nextSubtitle = None


    def addToFrequencyDistributionNoFreq(self, currSubtitleText, nextSubtitleText):
        tokens = []
        tokens = NLP.NLP.tokenize(currSubtitleText)

        size = len(tokens)
        wordResponse = WordResponse.WordResponse(nextSubtitleText, 1.0 / size)

        responses = []
        for token in tokens:
            #responses = set(WordResponse)
            responses.append(wordResponse)


    def addToFrequencyDistribution(self,frequencyDistribution, currSubtitleText, nextSubtitleText):
        tokens = NLP.NLP.tokenize(currSubtitleText)

        currSubtitleText = " ".join(currSubtitleText.split())
        nextSubtitleText = " ".join(nextSubtitleText.split())
        currSubtitleText = currSubtitleText.replace('-', '')
        nextSubtitleText = nextSubtitleText.replace('-', '')

        size = len(tokens)
        #print(nextSubtitleText)
        #print()
        wordResponse = WordResponse.WordResponse(nextSubtitleText, 1.0 / size)

        for token in tokens:
            responses = frequencyDistribution.get(token)
            if(responses == None):
                responses = set()

            responses.add(wordResponse)
            frequencyDistribution[token] = responses