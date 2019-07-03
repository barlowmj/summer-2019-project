from serial import Serial

class Board:

    def __init__(self, port_name):
        self.location = port_name
        self.ser = Serial(self.location)
        self.i_gain = None
        self.q_gain = None
        self.control_chip_str = None

    def init_control_chip(self):
        # turns OSK_EN on & freq mult to – necessary to control amplitude gain, and to get desired output frequency (respectively)
        # use this before set_thing, set_OSK_EN, set_freq_mult, set_work_mode
        self.ser.write(b'$WR0760004A000000B2*')
        self.control_chip_str = '$WR0760004A000000B2*'
        return

    def set_i_gain(self, i_gain):
        if i_gain > 4095 or i_gain < 0:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(i_gain, 'i')
        self.ser.write(command)
        self.i_gain = i_gain
        return

    def set_q_gain(self, q_gain):
        # sets quadrature output gain
        if q_gain > 4095 or q_gain < 1:
            print('Error: invalid gain value')
            return
        command = convert_mult_to_bytestring(q_gain, 'q')
        self.ser.write(command)
        self.q_gain = q_gain
        return

    def set_freq(self, f):
        clock = 300e6  # clock frequency in Hz
        n = 48  # bits of FTW
        ftw = int(f*((2**n)/clock))+1  # calculate frequency tuning word
        ftw_hex_str = str(hex(ftw))  # convert to hex string
        ftw_hex_str = ftw_hex_str[2:len(ftw_hex_str)]  # eliminate 0x at beginning
        while len(ftw_hex_str) < 12:
            ftw_hex_str = '0'+ftw_hex_str
        command = '$WR02'+ftw_hex_str[10:12]+ftw_hex_str[8:10]+ftw_hex_str[6:8]+ftw_hex_str[4:6]+ftw_hex_str[
                                                                                                 2:4]+ftw_hex_str[
                                                                                                      0:2]+'00*'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        return
        # sets frequency of board output, frquency input in Hz

    # WORK REQD – also figure out what it does?
    def set_thing(self, mode): # rename after you know what to call this !!!
        if mode == 'none':
            mode_bit = '0'
        elif mode == 'triangle':
            mode_bit = '2'
        elif mode == 'clr_acc1':
            mode_bit = '8'
        elif mode == 'clr_acc2':
            mode_bit = '4'
        else:
            print('Invalid input: please input one of \'none\', \'triangle\', \'clr_acc1\', or \'clr_acc2\'.')
            return
        self.control_chip_str = self.control_chip_str[0:7] + mode_bit + self.control_chip_str[8:20]
        self.ser.write(self.control_chip_str.encode('utf-8'))
        return

    def set_OSK_EN(self, power):
        if power == 'on':
            mode_bit = '6'
        elif power == 'off':
            mode_bit = '4'
        else:
            print('Invalid input: please input one of \'on\' or \'off\'.')
            return
        self.control_chip_str = self.control_chip_str[0:5] + mode_bit + self.control_chip_str[6:20]
        self.ser.write(self.control_chip_str.encode('utf-8'))
        return

    # WORK REQD
    def set_freq_mult(self, fq):
        if 1 < fq < 10 and isinstance(fq, int)==True:
            fq_str = str(hex(fq)).upper()
        else:
            print('Invalid input: please make sure that your frequency multiplier is an integer between 1 and 10.')
            return
        self.control_chip_str = self.control_chip_str[0:10] + fq_str + self.control_chip_str[11:20]
        self.ser.write(self.control_chip_str.encode('utf-8'))
        return

    # WORK REQD
    def set_work_mode(self, mode):
        if mode == 'single tone':
            mode_bit = '0'
        elif mode == 'fsk':
            mode_bit = '2'
        elif mode == 'ramped fsk':
            mode_bit = '4'
        elif mode == 'chirp':
            mode_bit = '6'
        else:
            print('Invalid input: please enter one of \'single tone\', \'fsk\', \'ramped fsk\', or \'chirp\'.')
            return
        self.control_chip_str = self.control_chip_str[0:8] + mode_bit + self.control_chip_str[9:20]
        self.ser.write(self.control_chip_str.encode('utf-8'))
        return

    # WORK REQD
    def set_freq2(self, f):
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

    # WORK REQD
    def set_delta_freq(self, f):
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


