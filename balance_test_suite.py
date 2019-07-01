from balance_functions import convert_mult_to_bytestring

'''
multiplier_test_vals = [-23, 32, 160, 575, 1001, 3460, 4095, 5000]
error_str1 = 'Error: invalid gain value'
expected_output = [None, '$WR0920000000000000*', '$WR09a0000000000000*', '$WR093f020000000000*', '$WR09e9030000000000*', '$WR09840d0000000000*', '$WR09ff0f0000000000*', None]
for i in range(len(multiplier_test_vals)):
    m_bs = convert_mult_to_bytestring(multiplier_test_vals[i], 'q')
    print(f'trial {i+1}:\nexpected output:', expected_output[i])
    print('actual output:', str(m_bs))
    print('length of the command in characters:', len(str(m_bs)),'\n')
# appears to be working !
'''


