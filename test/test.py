# sample for executing a C/++ program in python

from sh import Command
# sh library allows for use of Linux commands to execute other scripts
# sh.Command() allows returns command/function of form passed to it, must call resulting function to do anything

# opens directory
'''
cd = Command('cd', '/Users/jackbarlow/Desktop/test')
cd()
'''
# can also be written as follows:
cd = Command('cd')
directory = cd('/Users/jackbarlow/Desktop/test')

# compiles
gpp = Command('g++')
gpp('test.cpp', '-o', 'test')
run = Command('./test')
run()

# file stream, opens output file from C/++ program and reads data, storing the data in object 'end'
output = open('output.txt')
end = output.read()
print(end)
