
setList = []
actualList = []

actualFile = open("ramp chan2 measured.txt")
setFile = open("ramp chan2 set.txt")
totError = 0

for line in actualFile:
    actualList.append(float(line.strip()))

for line in setFile:
    setList.append(float(line.strip()))

for i in range (len(setList)):
    if (round(setList[i], 6) != 0):
        error = abs((actualList[i]-setList[i])/setList[i])
        totError += error


print (totError/len(setList))

