import visa
import time
import math

rm = visa.ResourceManager()
source= rm.open_resource('GPIB0::7::INSTR')
lockin= rm.open_resource('GPIB0::5::INSTR')

initAmp=.0002
tot=0
for i in range (1, 5):
    amp=i*initAmp
    source.write('SOUR:WAVE:AMPL '+str(amp))
    source.write('SOUR:WAVE:ARM')
    source.write('SOUR:WAVE:INIT')
    time.sleep(60)
    x=lockin.query_ascii_values('OUTP? 1')
    y=lockin.query_ascii_values('OUTP? 2')
    voltage= math.sqrt((x[0])**2+(y[0])**2)
    resistance= voltage/amp
    tot+=resistance
    print(resistance)
    source.write('SOUR:WAVE:ABOR')
    time.sleep(3)

print("Avg resistance= "+str(tot/i))
    

