import visa
from numpy import sqrt
import time

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::7::INSTR')
lockin = rm.open_resource('GPIB0::5::INSTR')

source.write('SOUR:WAVE:ABOR')

amp = .0002
for i in range(4):
    source.write(f'SOUR:WAVE:AMPL {amp}') # see if this works?
	source.write('SOUR:WAVE:ARM')
	source.write('SOUR:WAVE:INIT')
    time.sleep(60) # mess with time constant to see if this can be reduced
	x = lockin.query_ascii_values('OUTP? 1')
	y = lockin.query_ascii_values('OUTP? 2')
	volt = sqrt(x[0]**2 + y[0]**2)
	res = volt / amp
	print(res)
    source.write('SOUR:WAVE:ABOR') # does it need to be aborted each time or would changing the amplitude be sufficient? test this
	amp += 0.0002
    time.sleep(1.5) # see how short of a sleep period works
	






