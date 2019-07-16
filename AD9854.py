from serial import Serial

class Board:

    def __init__(self, port_name):
        self.location = port_name
        self.ser = Serial(self.location)
        self.i_gain = None
        self.q_gain = None
        self.control_chip_str = '00000000010010100000000001100000' # default value on power-up

    # turns off output for some reason
    def default(self):
        control_str = '00010000011001000000000100100000'
        command = convert_binary_to_control_chip_command(control_str)
        self.ser.write(command)
        self.control_chip_str = '00010000011001000000000100100000'
        return

    def i(self, i_gain):
        if i_gain > 4095 or i_gain < 1:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(i_gain, 'i')
        self.ser.write(command)
        self.i_gain = i_gain
        return

    def q(self, q_gain):
        if q_gain > 4095 or q_gain < 1:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(q_gain, 'q')
        self.ser.write(command)
        self.q_gain = q_gain
        return

    def f1(self, f):
        clock = 300e6  # clock frequency in Hz
        n = 48  # bits of FTW
        ftw = int(f*((2**n)/clock))+1  # calculate frequency tuning word
        ftw_hex_str = str(hex(ftw))  # convert to hex string
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]  # eliminate 0x at beginning
        while len(ftw_hex_str) < 12:
            ftw_hex_str = '0'+ftw_hex_str
        command = '$WR02'+ftw_hex_str[10:12]+ftw_hex_str[8:10]+ftw_hex_str[6:8]+ftw_hex_str[4:6]+ftw_hex_str[2:4]+ftw_hex_str[0:2]+'00*'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        return

    def f2(self, f):
        clock = 300e6
        n = 48
        ftw = int(f*((2**n)/clock))+1
        ftw_hex_str = str(hex(ftw))
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]
        while len(ftw_hex_str) < 12:
            ftw_hex_str = '0'+ftw_hex_str
        command = '$WR03'+ftw_hex_str[10:12]+ftw_hex_str[8:10]+ftw_hex_str[6:8]+ftw_hex_str[4:6]+ftw_hex_str[2:4]+ftw_hex_str[0:2]+'00*'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        return

    def del_f(self, f):
        clock = 300e6
        n = 48
        ftw = int(f*((2**n)/clock))+1
        ftw_hex_str = str(hex(ftw))
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]
        while len(ftw_hex_str) < 12:
            ftw_hex_str = '0'+ftw_hex_str
        command = '$WR04'+ftw_hex_str[10:12]+ftw_hex_str[8:10]+ftw_hex_str[6:8]+ftw_hex_str[4:6]+ftw_hex_str[2:4]+ftw_hex_str[0:2]+'00*'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        return

    def manual_set_control_chip(self, bin_control_str):
        # input string of binary values for all 32 bits written to the chip according to datasheet, ie bit 6 controls 'bypass inv sinc' – be careful using this
        if len(bin_control_str) != 32:
            print('Error: invalid bitstring length.')
            return
        for i in range(len(bin_control_str)):
            b = bin_control_str[i]
            if not (b == '1' or b == '0'):
                print('Error: invalid bistring.')
                return
        self.control_chip_str = bin_control_str
        command = convert_binary_to_control_chip_command(bin_control_str)
        self.ser.write(command)

        return

    def set_bit(self, bit_n, logic):
        # input bit numberset to logic high/low according to datasheet, ie bit 6 controls 'bypass inv sinc' – be careful using this
        if logic == 'high':
            bit = '1'
        elif logic == 'low':
            bit = '0'
        else:
            print('Error: invalid logic input.')
            return
        if bit_n > 31 or bit_n < 0:
            print('Error: invalid bit number.')
            return
        n = 31 - bit_n
        control_str = self.control_chip_str
        control_str = control_str[0:n] + bit + control_str[n+1:len(control_str)]
        self.control_chip_str = control_str
        command = convert_binary_to_control_chip_command(self.control_chip_str)
        self.ser.write(command)
        return

    def osk(self, power):
        if power == 'on':
            logic = 'high'
        elif power == 'off':
            logic = 'low'
        else:
            print('Error: invalid input. Make sure you inputted either \'on\' or \'off\'.')
            return
        self.set_bit(5, logic)
        return

    def f_sweep(self, power, f1=None, f2=None, delf=None):
        if power == 'on':
            tri_bit = '1'
            ramp_fsk_bit = '010'
        elif power == 'off':
            tri_bit = '0'
            ramp_fsk_bit = '000'
            return
        else:
            print('Error: invalid input. Make sure you inputted either \'on\' or \'off\'.')
            return
        self.f1(f1)
        self.f2(f2)
        self.del_f(delf)
        control_str = self.control_chip_str
        control_str = control_str[0:18] + tri_bit + control_str[19:20] + ramp_fsk_bit + control_str[23:len(control_str)] # does work mode str need to be reversed?
        command = convert_binary_to_control_chip_command(control_str)
        self.ser.write(command)
        return

    def f_mult(self, mult):
        if mult < 4 or mult > 20 or isinstance(mult, int) != True:
            print('Error: invalid input. Please enter an integer in the range 4 to (and including) 20.')
            return
        bin_mult_str = str(bin(mult))
        bin_mult_str = bin_mult_str[2:len(bin_mult_str)]
        if len(bin_mult_str) != 5:
            while len(bin_mult_str) < 5:
                bin_mult_str = '0' + bin_mult_str
        control_str = self.control_chip_str
        control_str = control_str[0:11] + bin_mult_str + control_str[16:len(control_str)] # does bin_mult_str need to be reversed?
        self.control_chip_str = control_str
        command = convert_binary_to_control_chip_command(self.control_chip_str)
        self.ser.write(command)
        return

    def work_mode(self, work_mode):
        if work_mode == 'single tone':
            bin_str = '000'
        elif work_mode == 'fsk':
            bin_str = '001'
        elif work_mode == 'ramped fsk':
            bin_str = '010'
        elif work_mode == 'chirp':
            bin_str = '011'
        elif work_mode == 'bpsk':
            bin_str = '100'
        else:
            print('Error: invalid input. Please enter one of \'single tone\', \'fsk\', \'ramped fsk\', \'chirp\', or \'bpsk\'.')
            return
        control_str = self.control_chip_str
        control_str = control_str[0:20] + bin_str + control_str[23:len(control_str)]
        self.control_chip_str = control_str
        command = convert_binary_to_control_chip_command(self.control_chip_str)
        self.ser.write(command)
        return

    def clracc1(self, power):
        if power == 'on':
            bit = '1'
        elif power == 'off':
            bit = '0'
        else:
            print('Error: invalid input.')
            return
        control_str = self.control_chip_str
        control_str = control_str[0:16] + bit + control_str[17:len(control_str)]
        self.control_chip_str = control_str
        command = convert_binary_to_control_chip_command(self.control_chip_str)
        self.ser.write(command)
        return


def convert_mult_to_bytestring(a, mul):
    # converts gain integer from 1 to 4095 into a command readable by the baord
    if mul == 'q':
        ser_add = '09'
    elif mul == 'i':
        ser_add = '08'
    else:
        print('Error: invalid input')
        return
    a_hex_str = str(hex(a)) # convert to hex string
    a_hex_str = a_hex_str[2:len(a_hex_str)] #eliminate 0x at beginning
    # must make it 4 digits
    while len(a_hex_str) < 4:
        a_hex_str = '0' + a_hex_str
    command = '$WR' + ser_add + a_hex_str[2:4] + a_hex_str[0:2] + '0000000000*' # amplitude multipliers always 4 digits
    command = command.upper()
    return command.encode('utf-8')

def convert_binary_to_control_chip_command(a):
    # a is 32-character string representing binary values
    byte1 = a[24:32]
    byte2 = a[16:24]
    byte3 = a[8:16]
    byte4 = a[0:8]
    bytes = [byte1, byte2, byte3, byte4]
    bytes_hex = []
    for byte in bytes:
        byte_hex = str(hex(int(byte,2)))
        byte_hex = byte_hex[2:len(byte_hex)].upper()
        if len(byte_hex) < 2:
            byte_hex = '0' + byte_hex
        bytes_hex.append(byte_hex)
    command = '$WR07' + bytes_hex[0] + bytes_hex[1] + bytes_hex[2] + bytes_hex[3] + '0000B2*'
    return command.encode('utf-8')








