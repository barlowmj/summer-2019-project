from serial import Serial

class Board:

    def __init__(self, port_name):
        self.location = port_name
        self.ser = Serial(self.location)

    def open(self):
        self.ser.open()
        return

    def set_control_chip(self):
        # turns on OSK_EN and sets frequency multiplier to x10
        self.ser.write(b'$WR0760004A000000B2*')
        return

    def set_i_gain(self, i_gain):

        if i_gain > 4095 or i_gain < 0:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(i_gain, 'i')
        self.ser.write(command)
        return

    def set_q_gain(self, q_gain):
        # sets quadrature output gain
        if q_gain > 4095 or q_gain < 1:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(q_gain, 'q')
        self.ser.write(command)
        return

    def set_freq(self, f):
        # sets frequency of board output, frquency input in Hz
        clock = 300e6  # clock frequency in Hz
        n = 48  # bits of FTW
        ftw = int(f * ((2**n) / clock)) + 1 # calculate frequency tuning word
        print(ftw)
        ftw_hex_str = str(hex(ftw))  # convert to hex string
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]  # eliminate 0x at beginning
        while len(ftw_hex_str) < 12:
            ftw_hex_str = '0' + ftw_hex_str
        command = '$WR02' + ftw_hex_str[10:12] + ftw_hex_str[8:10] + ftw_hex_str[6:8] + ftw_hex_str[4:6] + ftw_hex_str[2:4] + ftw_hex_str[0:2] + '00*'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        return

def convert_mult_to_bytestring(a, mul):
    # converts gain integer from 1 to 4095 into a command readable by the baord
    ser_add = '09' # default value, but be sure to input it
    if mul == 'q':
        ser_add = '09'
    elif mul == 'i':
        ser_add = '08'
    a_hex_str = str(hex(a)) # convert to hex string
    a_hex_str = a_hex_str[2:len(a_hex_str)] #eliminate 0x at beginning
    # must make it 4 digits
    while len(a_hex_str) < 4:
        a_hex_str = '0' + a_hex_str
    command = '$WR' + ser_add + a_hex_str[2:4] + a_hex_str[0:2] + '0000000000*' # amplitude multipliers always 4 digits
    command = command.upper()
    return command.encode('utf-8')


