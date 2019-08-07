import visa
import time as t
import serial
import numpy as np
import matplotlib.pyplot as plt


def sinWave(dataFile, multi, ser, chanNum, ampl):
    freq=1
    repeatNum = 3
    timeSteps=np.arange(0,repeatNum/freq,.02)
    voltage=ampl*np.sin(2*np.pi*freq*timeSteps)

    for i in range(timeSteps.size):
        commandStr='SET,'+str(chanNum)+','+str(voltage[i])+' \r'
        ser.write(commandStr.encode('utf-8'))
        t.sleep(.5)
        output = float(multi.query("READ?"))
        dataFile.write(str(output)+'\n')

    setValuesName = input("Enter the name for the set values file: ")
    np.savetxt(setValuesName, voltage, newline = '\n')
    offStr='SET, '+str(chanNum)+', 0 \r'
    ser.write(offStr.encode('utf-8'))
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
    ampl = float(input("Enter the amplitude voltage: "))
    voltage = sinWave(dataFile, multi, ser, chanNum, ampl)
    dataFile.close()

    plot(dataFileName, voltage)

    ser.close()

main()
