import visa
from numpy import sqrt, logspace, log10, zeros
import time
from pylab import plot, show, figure, xlabel, ylabel, title
from time_const import time_const

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::7::INSTR')
lockin = rm.open_resource('GPIB0::5::INSTR')

# freq_values = logspace(0.1, 100, num=20)
freq_values = [10, 50, 100, 500, 1000]
Vx_values = zeros(5)
Vy_values = zeros(5)

source.write('SOUR:WAVE:FUNC SIN')
source.write('SOUR:WAVE:AMPL 0.001')
source.write('SOUR:WAVE:PMAR:STAT ON')
source.write('SOUR:WAVE:PMAR:OLIN 1')
source.write(f'SOUR:WAVE:FREQ {freq_values[0]}')
lockin.write('PHAS 0.00')
source.write('SOUR:WAVE:ARM')
source.write('SOUR:WAVE:INIT')

for i in range(len(freq_values)):
    tau = time_const(freq_values[i])
    t = wait_time(tau)
    source.write(f'SOUR:WAVE:FREQ {freq_values[i]}')
    lockin.write(f'OFLT {tau}')
    time.sleep(t)
    vals = lockin.query_ascii_values('SNAP? 1,2')
    Vx = vals[0]
    Vy = vals[1]
    Vx_values[i] = Vx
    Vy_values[i] = Vy

source.write('SOUR:WAVE:ABOR')
res_x = Vx_values / 0.001
res_y = Vy_values / 0.001
cond_x = 1 / res_x
cond_y = 1 / res_y

figure(1)
plot(log10(freq_values), cond_x)
plot(log10(freq_values), cond_y)
show()

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








