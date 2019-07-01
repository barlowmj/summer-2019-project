from serial import Serial

class Board:

    def __init__(self, serial_address):
        self.address = serial_address

    def open(self):
        board = Serial(self.address)
        return board

    def OSK_EN_on(self):
        board = Board.open(self)
        board.write('$WR0760004A000000B2*')

    def set_i_gain(self, i_gain):
        if i_gain > 4095 or i_gain < 0:
            print('Error: invalid gain value')
            return
        board = Board.open(self)
        command = convert_mult_to_bytestring(i_gain, 'i')
        board.write(command)
        return

    def set_q_gain(self, q_gain):
        if q_gain > 4095 or q_gain < 0:
            print('Error: invalid gain value')
            return
        board = Board.open(self)
        command = convert_mult_to_bytestring(q_gain, 'q')
        board.write(command)
        return

    def set_freq_mult_10(self):
        board = Board.open(self)
        board.write('$WR0760004A')

    def set_freq(self, f):
        clock = 300e3  # clock frequency in Hz
        n = 48  # bits of FTW
        ftw = int(f*(2**n/clock))  # calculate frequency tuning word
        ftw_hex_str = str(hex(ftw))  # convert to hex string
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]  # eliminate 0x at beginning
        '''
        if len(ftw_hex_str)%2 != 0:
            ftw_hex_str = '0' + ftw_hex_str
        '''
        while len(ftw_hex_str) <= 12:
            ftw_hex_str = '0' + ftw_hex_str
        command = '$WR02' + ftw_hex_str[10:12] + ftw_hex_str[8:10] + ftw_hex_str[6:8] + ftw_hex_str[4:6] + ftw_hex_str[2:4] + ftw_hex_str[0:2] + '00*'
        board = Board.open(self)
        board.write(command)
        return

def convert_mult_to_bytestring(a, mul):
    ser_add = '09' # default value, but be sure to input it
    if mul == 'q':
        ser_add = '09'
    elif mul == 'i':
        ser_add = '08'
    a_hex_str = str(hex(a)) # convert to hex string
    a_hex_str = a_hex_str[2:len(a_hex_str)] #eliminate 0x at beginning
    # must make it 4 digits
    if len(a_hex_str) % 2 != 0:
        a_hex_str = '0' + a_hex_str
    elif len(a_hex_str) == 2:
        a_hex_str = '00' + a_hex_str
    print('status of string:', a_hex_str)
    command_str = '$WR' + ser_add + a_hex_str[2:4] + a_hex_str[0:2] + '0000000000*' # amplitude multipliers always 4 digits
    return command_str.encode('utf-8')


