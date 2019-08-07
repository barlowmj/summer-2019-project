import visa
import time as t
import serial
import numpy as np
import matplotlib.pyplot as plt


def ramp1(dataFile, multi, ser, chanNum, stVolt, endVolt, numSteps):
    multi.query("READ?") #Multimeter holds last result in output for some reason, so this removes it before taking actual measurements

    voltage = np.arange(stVolt, endVolt+(endVolt-stVolt)/numSteps, (endVolt-stVolt)/numSteps)
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        voltageAdj = voltage*1.000407503
        for x in np.nditer(voltageAdj, op_flags = ['readwrite']):
            if x < -10:
                x[...] = -10
            elif x >10:
                x[...] = 10
    else:
        voltageAdj = voltage*0.999360073

    for i in range(voltage.size):
        commandStr='SET,'+str(chanNum)+','+str(voltageAdj[i])+' \r'
        ser.write(commandStr.encode('utf-8'))
        t.sleep(.05)
        output = float(multi.query("READ?"))
        dataFile.write(str(output)+'\n')

    setValuesName = input("Enter the name for the set values file: ")
    np.savetxt(setValuesName, voltage, newline = '\n')
    commandStr='SET,'+str(chanNum)+',0 \r'
    ser.write(commandStr.encode('utf-8'))
    return voltage

def plot(dataFileName, voltage):
    resultsList = []
    diffList = []
    results = open(dataFileName, 'r')

    for line in results:
        resultsList.append(float(line.strip()))

    for i in range (len(resultsList)):
        diffList.append(resultsList[i]-voltage[i])

    measureNum = np.arange(0, len(resultsList),1)

    plt.figure(1)
    plt.plot(measureNum, resultsList, label = "Measured Voltage")
    plt.plot(measureNum, voltage, label = "Set Voltage")
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

    plt.show()
    results.close()

def main():
    rm = visa.ResourceManager()
    multi = rm.open_resource('GPIB0::3::INSTR')

    comPort=input("Please enter the com port for the Arduino Due: ")
    comPort = comPort.upper()
    timeout=int(input("Please enter the timeout length in seconds: "))
    ser = serial.Serial(comPort, 115200, timeout=timeout)

    dataFileName = input("Enter the the name for the measured values file: ")
    dataFile = open(dataFileName, 'w')

    chanNum = int(input("Enter the channel number: "))
    stVolt = float(input("Enter the starting voltage: "))
    endVolt = float(input("Enter the ending voltage: "))
    steps = int(input("Enter the number of steps: "))
    voltage = ramp1(dataFile, multi, ser, chanNum, stVolt, endVolt, steps)
    dataFile.close()

    plot(dataFileName,voltage)

    ser.close()

main()

    




