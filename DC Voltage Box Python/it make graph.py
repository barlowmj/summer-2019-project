import matplotlib.pyplot as plt
import numpy as np

resultsList = []
setVoltsList = []
diffList = []
percentDiff = []
resultsFile = input("Enter the name of the measured values file: ")
results = open(resultsFile)
setVoltsFile = input("Enter the name of the set voltage values file: ")
setVolts = open(setVoltsFile)

for line in results:
    resultsList.append(float(line.strip()))

for line in setVolts:
    setVoltsList.append(float(line.strip()))

measureNum = np.arange(0, len(resultsList), 1)

for i in range (len(resultsList)):
    diffList.append(resultsList[i]-setVoltsList[i])
    if (round(setVoltsList[i],6) != 0):
        #percentDiff.append(abs(diffList[i]/setVoltsList[i]*100))
        percentDiff.append(diffList[i]/setVoltsList[i]*100)
    else:
        percentDiff.append(0)


plt.figure(1)
plt.plot(measureNum, resultsList, label = "Measured Voltage")
plt.plot(measureNum, setVoltsList, label = "Set Voltage")
title1 = input("Enter a title for the plot the measured/set plot: ")
plt.title(title1)
plt.xlabel("Measurement #")
plt.ylabel("Voltage")
plt.legend(loc = 'best')

plt.figure(2)
plt.plot(measureNum, diffList)
title2 = input("Enter a title for the measured/set difference plot: ")
plt.title(title2)
plt.xlabel("Measurement #")
plt.ylabel("Difference (V)")

plt.figure(3)
plt.plot(setVoltsList, diffList)
title3 = input("Enter a title for the difference vs set voltage plot: ")
plt.title(title3)
plt.xlabel("Set Voltage (V)")
plt.ylabel("Difference (V)")

plt.figure(4)
plt.plot(setVoltsList, percentDiff)
title4 = input("Enter a title for the percent difference vs set voltage plot: ")
plt.title(title4)
plt.xlabel("Set Voltage (V)")
plt.ylabel("Percent Difference")

plt.show()

