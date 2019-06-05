import visa
from numpy import sqrt
import time

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::7::INSTR')
lockin = rm.open_resource('GPIB0::5::INSTR')

source.write('SOUR:WAVE:ABOR')

source.write('SOUR:WAVE:FUNC SIN')
source.write('SOUR:WAVE:FREQ 500')
source.write('SOUR:WAVE:PMAR:STAT ON')
source.write('SOUR:WAVE:PMAR:OLIN 1')
lockin.write('PHAS 0.00')
lockin.write('OFLT 6')
time.sleep(1)
source.write('SOUR:WAVE:ARM')
source.write('SOUR:WAVE:INIT')

amp = .0004
for i in range(4):
    source.write(f'SOUR:WAVE:AMPL {amp}') # see if this works?
    time.sleep(0.1) # mess with time constant to see if this can be reduced
    vals = lockin.query_ascii_values('SNAP? 1,2')
    volt = sqrt(vals[0]**2 + vals[1]**2)
    res = volt / amp
    print(res)
    amp += 0.0002
    time.sleep(1) # see how short of a sleep period works

