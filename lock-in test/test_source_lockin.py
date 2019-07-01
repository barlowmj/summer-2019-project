import visa
from numpy import sqrt, logspace, log10, zeros
from time import sleep
from pylab import plot, show, figure, xlabel, ylabel, title, legend
from time_constant import time_const
from wait_time import wait_time

f_start = 2.5
f_end = 4.8
length = 500
amp = 0.002

freq_values = logspace(f_start, f_end, num=length)
for f in freq_values:
    f = round(f, 3)

Vx_values = zeros(length)
Vy_values = zeros(length)

rm = visa.ResourceManager()
source = rm.open_resource('GPIB0::7::INSTR')
lockin = rm.open_resource('GPIB0::5::INSTR')

source.write('SOUR:WAVE:FUNC SIN')
source.write(f'SOUR:WAVE:AMPL {amp}')
source.write('SOUR:WAVE:PMAR:STAT ON')
source.write('SOUR:WAVE:PMAR:OLIN 1')
source.write(f'SOUR:WAVE:FREQ {freq_values[0]}')
lockin.write('PHAS 0.00')

source.write('SOUR:WAVE:ARM')
source.write('SOUR:WAVE:INIT')

for i in range(length):
    tau = time_const(freq_values[i])
    t = wait_time(tau)
    source.write(f'SOUR:WAVE:FREQ {freq_values[i]}')
    lockin.write(f'OFLT {tau}')
    sleep(t+1)
    vals = lockin.query_ascii_values('SNAP? 1,2')
    Vx_values[i] = vals[0]
    Vy_values[i] = vals[1]

source.write('SOUR:WAVE:ABOR')

res_x = Vx_values / amp
res_y = Vy_values / amp

figure(1)
plot(log10(freq_values), res_x)
plot(log10(freq_values), res_y)
legend([r'$\rho_x$', r'$\rho_y$'])
title('resistance')

cond_x = res_x**(-1)
cond_y = res_y**(-1)

'''
figure(2)
plot(log10(freq_values), abs(cond_x))
plot(log10(freq_values), abs(cond_y))
legend(['$\sigma_x$', '$\sigma_y$'])
title('conductivity')
'''

figure(2)
plot(log10(freq_values), abs(cond_x))
title('$\sigma_x$')

figure(3)
plot(log10(freq_values), abs(cond_y))
title('$\sigma_y$')

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








