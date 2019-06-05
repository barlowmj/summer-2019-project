import visa
from numpy import sqrt, logspace
import time
from pylab import plot, show, figure, xlabel, ylabel, title

def time_const(f):
    if f > 5e5:
        return 0
    elif f > (1e6)/6:
        return 1
    elif f > 5e4:
        return 2
    elif f > (1e5)/6:
        return 3
    elif f > 5e3:
        return 4
    elif f > (1e4)/6:
        return 5
    elif f > 5e2:
        return 6
    elif f > (1e3)/6:
        return 7
    elif f > 5e1:
        return 8
    elif f > (1e2)/6:
        return 9
    elif f > 5:
        return 10
    elif f > (1e1)/6:
        return 11
    elif f > 5e-1:
        return 12
    elif f > 1/6:
        return 13
    elif f > 5e-2:
        return 14
    elif f > (1e-1)/6:
        return 15
    elif f > 5e-3:
        return 16
    elif f > (1e-2)/6:
        return 17
    elif f > 5e-4:
        return 18
    elif f > (1e-3)/6:
        return 19

def wait_time(tau):
if tau == 0:
    return 5*10e-6
elif tau == 1:
    return 5*30e-6
elif tau == 2:
    return 5*10e-5
elif tau == 3:
    return 5*30e-5
elif tau == 4:
    return 5*10e-4
elif tau == 5:
    return 5*30e-4
elif tau == 6:
    return 5*10e-3
elif tau == 7:
    return 5*30e-3
elif tau == 8:
    return 5*10e-2
elif tau == 9:
    return 5*30e-2
elif tau == 10:
    return 5*10e-1
elif tau == 11:
    return 5*30e-1
elif tau == 12:
    return 5*10
elif tau == 13:
    return 5*30
elif tau == 14:
    return 5*10e1:
elif tau == 15:
    return 5*30e1
elif tau == 16:
    return 5*10e2
elif tau == 17:
    return 5*30e2
elif tau == 18:
    return 5*10e3
elif tau == 19:
    return 5*30e3

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::7::INSTR')
lockin = rm.open_resource('GPIB0::5::INSTR')

'''
source.write('SOUR:WAVE:FUNC SIN')
source.write('SOUR:WAVE:FREQ 500')
source.write('SOUR:WAVE:PMAR:STAT ON')
source.write('SOUR:WAVE:PMAR:OLIN 1')
lockin.write('PHAS 0.00')
lockin.write('OFLT 6')
time.sleep(1)
source.write('SOUR:WAVE:ARM')
source.write('SOUR:WAVE:INIT')

amp_vals = []
volt_vals = []
res_vals = []
amp = 0.0004
for i in range(20):
    amp_vals.append(amp)
    source.write(f'SOUR:WAVE:AMPL {amp}') # see if this works?
    time.sleep(0.075) # mess with time constant to see if this can be reduced
    vals = lockin.query_ascii_values('SNAP? 1,2')
    volt = sqrt(vals[0]**2 + vals[1]**2)
    volt_vals.append(volt)
    res = volt / amp
    res_vals.append(res)
    amp += 0.00002
    time.sleep(1)

source.write('SOUR:WAVE:ABOR')

avg_res = sum(res_vals) / len(res_vals)
figure(1)
plot(amp_vals, res_vals)
xlabel('current')
ylabel('resitance')
title('resitance vs. current amplitude')

figure(2)
plot(amp_vals, volt_vals)
xlabel('current')
ylabel('voltage')
title('voltage vs current')

show()
'''

freq_values = logspace(10e-3, 10e3, num=20)
Vx_values = []
Vy_values = []

source.write('SOUR:WAVE:FUNC SIN')
source.write('SOUR:WAVE:AMPL 0.5')
source.write('SOUR:WAVE:PMAR:STAT ON')
source.write('SOUR:WAVE:PMAR:OLIN 1')
source.write(f'SOUR:WAVE:FREQ {freq_values[-1]}')
lockin.write('PHAS 0.00')
time.sleep(1)
source.write('SOUR:WAVE:ARM')
source.write('SOUR:WAVE:INIT')

for f in freq_values:
    tau = time_const(f)
    t = wait_time(tau)
    source.write(f'SOUR:WAVE:FREQ {f}')
    lockin.write(f'OFLT {tau}')
    time.sleep(t)
    vals = lockin.query_ascii_values('SNAP? 1,2')
    Vx = vals[0]
    Vy = vals[1]










