from balance_functions import convert_mult_to_bytestring
from numpy import arange
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
for m in mult_vals_b:
    board.write(m)
    voltage = lockin.query_ascii_values('SNAP? 1,2')
