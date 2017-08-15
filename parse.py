import codecs,re,sys

fileName = sys.argv[1]
try:
    measureGroup = sys.argv[2]
except IndexError:
    measureGroup=""

startMemberDefine = "CREATE MEMBER CURRENTCUBE"
endMemberDefine = "ASSOCIATED_MEASURE_GROUP = '"+measureGroup+"'"
memberBody = False
skipFirstLine = False


class MeasuresArray:
    def __init__(self):
        self.measures = []
    def contain(self,text):
        try:
            self.measures.index(text)
        except ValueError:
            self.measures.append(text)
    def clearFromCalc(self,calc):
        try:
            index = self.measures.index(calc)
            self.measures.pop(index)
        except ValueError:
            pass
    def printMeasAr(self):
        for meas in self.measures:
            print(meas + ',')

class Member:
    def __init__(self):
        self.memberBody = ""
        self.pattern = re.compile('[[]Measures[]].[[][\sа-яА-Яa-zA-Z0-9_-]*[]]')
    def appendLine(self,line):
        self.memberBody = self.memberBody+line
    def readMeasures(self,measAr):
        for measure in re.findall(self.pattern, self.memberBody):
            measAr.contain(measure)

calculated = []
measArr = MeasuresArray()
mdx = codecs.open(fileName,"r","utf-8")
patternMeas = re.compile('[[]Measures[]].[[][\sа-яА-Яa-zA-Z0-9_-]*[]]')
readMember = Member()
for line in mdx:
    if startMemberDefine in line:
        skipFirstLine = True
        readMember = Member()
        calcMeasure = re.findall(patternMeas,line)
        for calcul in calcMeasure:
            calculated.append(calcul)
    if endMemberDefine in line:
        memberBody = False
        readMember.readMeasures(measArr)
    if memberBody:
        readMember.appendLine(line)
    if skipFirstLine:
        skipFirstLine = False
        memberBody = True

print("-------All measures-------")
measArr.printMeasAr()
print("------Not calculated------")
for calc in calculated:
    measArr.clearFromCalc(calc)
measArr.printMeasAr()






