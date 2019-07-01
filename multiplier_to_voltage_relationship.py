from balance_functions import convert_mult_to_bytestring
from numpy import arange, array
from numpy.linalg import norm
from pylab import plot, xlabel, ylabel, title, figure
import time
import serial
import visa

board_location = '/dev/cu.wchusbserial145410'
board = serial.Serial(board_location)

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR')

mult_vals = arange(0, 4096, 1)
mult_vals_b = []
for i in range(len(mult_vals)):
    mult_vals_b.append(convert_mult_to_bytestring(mult_vals[i], 'q'))

vx_vals = []
vy_vals = []
voltage_vals = []
for m in mult_vals_b:
    board.write(m)
    time.sleep(1) # change depending on time constant of lock-in
    voltage = lockin.query_ascii_values('SNAP? 1,2', container=array)
    vx_vals.append(voltage[0])
    vy_vals.append(voltage[1])
    voltage_vals.append(norm(voltage))

figure(1)
plot(mult_vals, voltage_vals)
xlabel('Multiplier value')
ylabel('Voltage amplitude')
title('Voltage vs Multiplier value')

figure(2)
plot(mult_vals, vx_vals)
xlabel('Multiplier value')
ylabel('x-component of voltage amplitude')
title(f'V_x vs Multiplier value')

figure(3)
plot(mult_vals, vy_vals)
xlabel('Multiplier value')
ylabel('y-component of voltage amplitude')
title(f'V_y vs Multiplier value')
