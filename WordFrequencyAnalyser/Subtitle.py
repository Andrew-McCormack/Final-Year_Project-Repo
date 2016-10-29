class Subtitle:

    subtitleNumber = 0
    startTime = 0
    stopTime = 0
    subtitleString = ''

    def __init__(self, subtitleNumber, startTime, stopTime, subtitleString):
        self.subtitleNumber = subtitleNumber
        self.startOfSubtitle = startTime
        self.endOfSubtitle = stopTime
        self.subtitleString = subtitleString

    def printSub(self):
        print(self.subtitleString)