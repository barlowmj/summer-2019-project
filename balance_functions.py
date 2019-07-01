# functions that will be used in balance.py

def convert_mult_to_bytestring(a, mul):
    ser_port = '09' # default value, but be sure to input it
    if a > 4095 or a < 0:
        print('Error: invalid gain value')
        return
    if mul == 'q':
        ser_port = '09'
    elif mul == 'i':
        ser_port = '08'
    a_hex_str = str(hex(a)) # convert to hex string
    a_hex_str = a_hex_str[2:len(a_hex_str)] #eliminate 0x at beginning

    # must make it 4 digits
    if len(a_hex_str) % 2 != 0:
        a_hex_str = '0' + a_hex_str
    elif len(a_hex_str) == 2:
        a_hex_str = '00' + a_hex_str
    print('status of string:', a_hex_str)
    command_str = '$WR' + ser_port + a_hex_str[2:4] + a_hex_str[0:2] + '0000000000*' # amplitude multipliers always 4 digits
    return command_str.encode('utf-8')

