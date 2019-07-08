from AD9854 import Board
import time

location =  '/dev/cu.wchusbserial145410'
b = Board(location)

b.init_control_chip()
time.sleep(2)
b.set_i_gain(1000)
time.sleep(10)
b.set_i_gain(2000)





