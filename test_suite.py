from AD9854_AC_board import Board
import time

board = Board('/dev/cu.wchusbserial145410')
board.set_control_chip()
time.sleep(5)
board.set_freq(7000)
time.sleep(5)
board.set_freq(5000000)
time.sleep(5)
board.set_i_gain(3476)
time.sleep(5)
board.set_q_gain(950)





