#Code for controlling the Seekat (Ardunio Due) 16 channel voltage source
#Channels 2,3,6,7 will provide more accurate output due to the other channels undershooting,
#which makes correcting them near -10V and 10V difficult
#See http://opendacs.com/seekat-with-arduino-due-homepage-2/how-to-communicate-with-the-dcbox/
#for string formatting for Seekat commands
#Written by Aric Moilanen
#Last Edited: 7/31/2019 by Aric Moilanen

import serial
import numpy as np
import time 

#Generates a sin wave of provided amplitude and frequency. The wave can be made more
#continous by decreasing step sizes but below 13 ms it will not be able keep time correctly
#as time.sleep() does not work correctly below that value.
#Right now, this function does not scale correctly with time. It can produce a sin wave,
#but it will not be of specified frequency or for the correct time length.
def sinWave(ser, chanNum, ampl, freq, timeLength):
    #Creates a numpy array of time values for generating the sin wave.
    #Step size should match the time.sleep() later on in an attempt
    #to keep the wave synced with real time.
    timeSteps=np.arange(0,timeLength,.02)
    
    #Generate a numpy array of voltage sin values based on freq and ampl
    voltage=ampl*np.sin(2*np.pi*freq*timeSteps)

    #Applies adjustment to voltage values to reduce error. Channels controlled
    #by board 1 (0,1,4,5) undershoot while the rest overshoot.
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        voltage = voltage*1.000407503
        #Command fails if you attempt to set a voltage <-10 or >10, so this
        #ensures all voltage values fall within that range after they've been
        #adjusted. This is only a problem for board 1 channels since the
        #adjustment makes them larger.
        for x in np.nditer(voltage, op_flags = ['readwrite']):
            if x < -10:
                x[...] = -10
            elif x >10:
                x[...] = 10
    else:
        voltage = voltage*0.999360073

    #Sends the set voltage command for each value generated previously
    for i in range(voltage.size):
        #Assembles the "SET" command string to send to the DUE
        commandStr='SET,'+str(chanNum)+','+str(voltage[i])+' \r'
        #Encodes command string to bytes before passing to the DUE 
        ser.write(commandStr.encode('utf-8'))
        time.sleep(.02)
        response = ser.readline()

    #Set the output channel back to 0V
    offStr='SET, '+str(chanNum)+', 0 \r'
    ser.write(offStr.encode('utf-8'))
    response = ser.readline()
    
    print("Operation finished")
    
#Generates a square wave of given amplitude and period for a given length of time.
#Will only work correctly if the timeLength is a multiple of period.
def sqWave(ser, chanNum, ampl, period, timeLength):
    #Resets channel to 0V before passing commands
    offStr='SET, '+str(chanNum)+', 0 \r'
    ser.write(offStr.encode('utf-8'))
    time.sleep(1)

    #Applies adjustment to voltage value to reduce error. Channels controlled
    #by board 1 (0,1,4,5) undershoot while the rest overshoot.
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        ampl = ampl*1.000407503
        if (ampl > 10):
            ampl = 10
        elif (ampl <-10):
            ampl = -10
    else:
        ampl = ampl*0.999360073

    for i in range(int(timeLength/period)):
        #Generates "SET" command to change output to amplitude voltage,
        #encodes to bytes, and passes to DUE
        commandStr='SET,'+str(chanNum)+','+str(ampl)+' \r'
        ser.write(commandStr.encode('utf-8'))
        #Keep at amplitude voltage for half of one period
        time.sleep(period*.5)
        response = ser.readline()

        #Resets channel to 0V for half of one period
        ser.write(offStr.encode('utf-8'))
        time.sleep(period*.5)
        response= ser.readline()

    #Sets channel back to 0V
    ser.write(offStr.encode('utf-8'))
    time.sleep(.02)
    response = ser.readline()
        
    print("Operation finished")

#Generates a sawtooth wave with a given starting and end voltage. As of now, only repeats
#the wave 5 times, with each period lasting ~(highVolt-lowVolt) seconds
def sawWave(ser, chanNum, lowVolt, highVolt):
    #How many periods the wave will repeat for
    repeatNum = 5
    
    #Generates an array of voltage values for one period of
    #the sawtooth wave. The step size should match the
    #time.sleep() values in order to keep sync with real time.
    voltage = np.arange(lowVolt, highVolt+.02, .02)

    #Applies adjustment to voltage values to reduce error. Channels controlled
    #by board 1 (0,1,4,5) undershoot while the rest overshoot.
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        voltage = voltage*1.000407503
        #Command fails if you attempt to set a voltage <-10 or >10, so this
        #ensures all voltage values fall within that range after they've been
        #adjusted. This is only a problem for board 1 channels since the
        #adjustment makes them larger.
        for x in np.nditer(voltage, op_flags = ['readwrite']):
            if x < -10:
                x[...] = -10
            elif x >10:
                x[...] = 10
    else:
        voltage = voltage*0.999360073
    
    #This extends the voltage array by repeating it repeatNum times
    voltage = np.tile(voltage, repeatNum)

    #Iterates thru the voltage array, passing the appropriate "SET" commands
    #for each value
    for i in range (voltage.size):
        commandStr='SET,'+str(chanNum)+','+str(voltage[i])+' \r'
        ser.write(commandStr.encode('utf-8'))
        time.sleep(.02)
        response= ser.readline()

    #Sets the output channel to 0V and reads all previous output from the buffer
    offStr='SET, '+str(chanNum)+', 0 \r'
    ser.write(offStr.encode('utf-8'))
    response = ser.readline()
    #response.strip()
    #while (len(response) > 0):
        #response = ser.readline()
        #response.strip()
    print("Operation finished")

#Reads the voltage set on a given channel
def readChannel(ser, chanNum):
    commandStr='GET_DAC,'+str(chanNum)+' \r'
    ser.write(commandStr.encode('utf-8'))
    time.sleep(.02)
    #Prints response from Seekat with trailing characters stripped
    print(ser.readline().strip())

#Sets the voltage of one output channel
def setChannel(ser, chanNum, volt):
    #Applies adjustment to voltage value to reduce error. 
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        volt = volt*1.000407503
        if (volt > 10):
            volt = 10
        elif (volt <-10):
            volt = -10
    else:
        volt = volt*0.999360073
    
    commandStr='SET,'+str(chanNum)+','+str(volt)+' \r'
    ser.write(commandStr.encode('utf-8'))
    time.sleep(.02)
    #Prints response from Seekat with trailing characters stripped
    print(ser.readline().strip())

#Ramps one channel using given start and end voltages, # of steps, and delay time between
#steps. Channel will remain at endVolt after the ramp is finished.
#This function can't be adjusted to reduce error as it uses a built in
#Seekat operation which does not allow you to access the voltage values.
def ramp1(ser, chanNum, stVolt, endVolt, numSteps, delayTime):
    commandStr='RAMP1,'+str(chanNum)+','+str(stVolt)+','+str(endVolt)+','+str(numSteps)+','+str(delayTime)+' \r'
    ser.write(commandStr.encode('utf-8'))
    #Waits until operations is finished, converts delayTime to seconds from microseconds in
    #order to work with time.sleep()
    time.sleep(numSteps*delayTime*(10**(-6))+.1)
    #Prints response from Seekat with trailing characters stripped
    print(ser.readline().strip())

#Ramps two channels simultaneously. numSteps needs to be the TOTAL number of steps
#for both channels, not the number of steps you want for each channel.
#Both channels will remain at endVolt once the ramp is finished.
#This function can't be adjusted to reduce error as it uses a built in
#Seekat operation which does not allow you to access the voltage values.
def ramp2(ser, chanNum1, chanNum2, stVolt1, stVolt2, endVolt1, endVolt2, numSteps, delayTime):
    commandStr='RAMP1,'+str(chanNum1)+','+str(chanNum2)+','+str(stVolt1)+','+str(stVolt2)+','+str(endVolt1)+','+str(endVolt2)+','+str(numSteps)+','+str(delayTime)+' \r'
    ser.write(commandStr.encode('utf-8'))
    time.sleep(.02)
    #Only sleep half the time since numSteps is double what either channel is doing
    time.sleep(.5*numSteps*delayTime*(10**(-6))+.1)
    #Prints response from Seekat with trailing characters stripped
    print(ser.readline().strip())

#This ramp function has to voltage adjustment but can not take a delay time <13ms due to
#time.sleep() limitations.
def rampAdj(ser, chanNum, stVolt, endVolt, numSteps, delayTime):
    #Generates an array of voltage values between the start and end voltage, with an
    #appropriate step size for the given number of steps.
    #The end voltage has the added (endVolt-stVolt)/numSteps since np.arange() does
    #not include the end value by default, so we need to go one step past where we want
    #to end.
    voltage = np.arange(stVolt, endVolt+(endVolt-stVolt)/numSteps, (endVolt-stVolt)/numSteps)

    #Voltage adjustment
    if (chanNum == 0 or chanNum == 1 or chanNum == 4 or chanNum == 5):
        voltage = voltage*1.000407503
        for x in np.nditer(voltage, op_flags = ['readwrite']):
            if x < -10:
                x[...] = -10
            elif x >10:
                x[...] = 10
    else:
        voltage = voltage*0.999360073

    #Passes "SET" commands for each voltage values with the delay time between each command
    for i in range(voltage.size):
        commandStr='SET,'+str(chanNum)+','+str(voltage[i])+' \r'
        ser.write(commandStr.encode('utf-8'))
        time.sleep(delayTime)
        response=ser.readline()

    #Sets channel back to 0V and reads responses from the buffer
    commandStr='SET,'+str(chanNum)+',0 \r'
    ser.write(commandStr.encode('utf-8'))
    response = ser.readline()
    print("Operation finished")

#Print the IDN for the Seekat
def IDN(ser):
    ser.write(b'*IDN? \r')
    time.sleep(.02)
    #Prints response from Seekat with trailing characters stripped
    print(ser.readline().strip())
    
def main():
    #Gets comPort for Arduino Due from user. This can be found in the Device Manager
    #or the Arduino IDE serial monitor.
    comPort=input("Please enter the com port for the Arduino Due: ")
    #Gets timeout length from user input
    timeout=int(input("Please enter the timeout length in seconds: "))
    #Opens serial connection with Arduino Due
    ser = serial.Serial(comPort, 115200, timeout=timeout)

    print("Please enter a command from the following list: ")
    cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
    cmd = cmd.lower()

    while (cmd != 'exit'):
        if (cmd == 'idn'):
            IDN(ser)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()
            
        elif (cmd == 'set'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            volt = float(input("Please enter the voltage: "))
            while (volt < -10 or volt >10):
                volt = float(input("Enter a valid voltage between -10V and 10V: "))
            setChannel(ser, chanNum, volt)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()
            
        elif (cmd == 'read'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            readChannel(ser, chanNum)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()
            
        elif (cmd == 'ramp1'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            stVolt = float(input("Please enter the starting voltage: "))
            while (stVolt < -10 or stVolt >10):
                stVolt = float(input("Enter a valid starting voltage between -10V and 10V: "))
            endVolt = float(input("Please enter the ending voltage: "))
            while ((endVolt < -10 or endVolt >10) or endVolt < stVolt):
                endVolt = float(input("Enter a valid starting ending between -10V and 10V that is larger than the starting voltage: "))
            numSteps = int(input("Please enter the number of steps: "))
            while (numSteps <= 0):
                numSteps = int(input("Enter a number of steps greater than 0: "))
            delayTime= float(input("Please enter the delay time in microseconds: "))
            while (delayTime <= 0):
                delayTime = float(input("Enter a delay time greater than 0: "))
            ramp1(ser, chanNum, stVolt, endVolt, numSteps, delayTime)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()
            
        elif (cmd == 'ramp2'):
            chanNum1 = int(input("Please enter the first channel number: "))
            while (chanNum1 < 0 or chanNum1 > 7):
                chanNum1 = int(input("Enter a valid channel number 0-7: "))
            chanNum2 = int(input("Please enter the second channel number: "))
            while (chanNum2 < 0 or chanNum2 > 7):
                chanNum2 = int(input("Enter a valid channel number 0-7: "))
            stVolt1 = float(input("Please enter the starting voltage for the first channel: "))
            while (stVolt1 < -10 or stVolt1 >10):
                stVolt1 = float(input("Enter a valid starting voltage between -10V and 10V: "))
            stVolt2 = float(input("Please enter the starting voltage for the second channel: "))
            while (stVolt2 < -10 or stVolt2 >10):
                stVolt2 = float(input("Enter a valid starting voltage between -10V and 10V: "))
            endVolt1 = float(input("Please enter the ending voltage for the first channel: "))
            while ((endVolt1 < -10 or endVolt1 >10) or endVolt1 < stVolt1):
                endVolt1 = float(input("Enter a valid starting ending between -10V and 10V that is larger than the starting voltage: "))
            endVolt2 = float(input("Please enter the ending voltage for the second channel: "))
            while ((endVolt2 < -10 or endVolt2 >10) or endVolt2 < stVolt2):
                endVolt2 = float(input("Enter a valid starting ending between -10V and 10V that is larger than the starting voltage: "))
            numSteps = int(input("Please enter the combined number of steps for both channels: "))
            while (numSteps <= 1):
                numSteps = int(input("Enter a number of steps greater than or equal to 2: "))
            delayTime= float(input("Please enter the delay time in microseconds: "))
            while (delayTime <= 0):
                delayTime = float(input("Enter a delay time greater than 0: "))
            ramp1(ser, chanNum, stVolt, endVolt, numSteps, delayTime)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()

        elif (cmd =='rampadj'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            stVolt = float(input("Please enter the starting voltage: "))
            while (stVolt < -10 or stVolt >10):
                stVolt = float(input("Enter a valid starting voltage between -10V and 10V: "))
            endVolt = float(input("Please enter the ending voltage: "))
            while ((endVolt < -10 or endVolt >10) or endVolt < stVolt):
                endVolt = float(input("Enter a valid starting ending between -10V and 10V that is larger than the starting voltage: "))
            numSteps = int(input("Please enter the number of steps: "))
            while (numSteps <= 0):
                numSteps = int(input("Enter a number of steps greater than 0: "))
            delayTime= float(input("Please enter the delay time in seconds: "))
            while (delayTime < 0.013):
                delayTime = float(input("Enter a delay time greater than 13ms: "))
            rampAdj(ser, chanNum, stVolt, endVolt, numSteps, delayTime)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()
            

        elif (cmd == 'sqwave'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            ampl = float(input("Please enter the amplitude voltage of the square wave: "))
            while (ampl <= 0):
                ampl = float(input("Enter an amplitude voltage greater than zero: "))
            period = float(input("Please enter the period in seconds: "))
            while (period <= 0):
                period = float(input("Enter a period greater than zero: "))
            timeLength = float(input("Please enter how long you would like to generate the wave for in seconds: "))
            while (timeLength <= 0):
                timeLength = float(input("Enter a time greater than zero: "))
            sqWave(ser, chanNum, ampl, period, timeLength)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()

        elif (cmd == 'sinwave'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            ampl = float(input("Please enter the amplitude voltage of the sin wave: "))
            while (ampl <= 0):
                ampl = float(input("Enter an amplitude voltage greater than zero: "))
            freq = float(input("Please enter the frequency of the sin wave in Hz: "))
            while (freq <= 0):
                freq = float(input("Enter a frequency greater than zero: "))
            timeLength = float(input("Please enter how long you would like to generate the wave for in seconds: "))
            while (timeLength <= 0):
                timeLength = float(input("Enter a time greater than zero: "))
            sinWave(ser, chanNum, ampl, freq, timeLength)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()

        elif (cmd == 'sawwave'):
            chanNum = int(input("Please enter the channel number: "))
            while (chanNum < 0 or chanNum > 7):
                chanNum = int(input("Enter a valid channel number 0-7: "))
            lowVolt = float(input("Please enter the low voltage: "))
            while (lowVolt <-10 or lowVolt > 10):
                lowVolt = float(input("Please enter a voltage between -10V and 10V: "))
            highVolt = float(input("Please enter the high voltage: "))
            while (highVolt <-10 or highVolt >10 or highVolt < lowVolt):
                highVolt = float(input("Please enter a voltage between -10V and 10V that is higher than the low voltage: "))
            sawWave(ser, chanNum, lowVolt, highVolt)
            print("")
            print("Please enter a command from the following list: ")
            cmd = input("IDN, SET, READ, RAMP1, RAMP2, RAMPADJ, sqWave, sinWave, sawWave, Exit \n")
            cmd = cmd.lower()

        else:
            cmd = input("Command not valid. Please enter the command again: ")
            cmd = cmd.lower()

    #Sets all channels to 0V then closes serial connection  
    ser.write(b'SET,0,0 \r')
    ser.write(b'SET,1,0 \r')
    ser.write(b'SET,2,0 \r')
    ser.write(b'SET,3,0 \r')
    ser.write(b'SET,4,0 \r')
    ser.write(b'SET,5,0 \r')
    ser.write(b'SET,6,0 \r')
    ser.write(b'SET,7,0 \r')
    ser.close()

main()
            
            
            
            
            
            
            
            
                
                           
                
                
                              
                              
            
                          
    
    

    

    
    

    
        

    
    
    
    
    
    
