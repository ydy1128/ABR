#!/usr/bin/env python
'''dump_asm.py - Simple XED2 based disassembler.'''

__author__ = 'huku <huku@grhack.net>'

#modified from the program from pyxed module examples called dump_asm.py
#source of pyxed module: https://github.com/huku-/pyxed

import sys
import binascii
import random

import pyxed


def getRanInt(length):
    rand = random.randint(0, length)
    if rand % 2 != 0:
        rand += 1
    return rand

def openFile(name):
    f = open(name, 'rb')
    data = f.read()
    # hex_data = str(binascii.hexlify(data))
    # var = hex_data[2:-1]
    # f.close()
    return data

def decode(ar, start_point):
    string = ''
    xed = pyxed.Decoder()
    xed.set_mode(pyxed.XED_MACHINE_MODE_LEGACY_32, pyxed.XED_ADDRESS_WIDTH_32b)
    # xed.itext = binascii.unhexlify(ar)
    xed.itext = ar
    xed.runtime_address = start_point

    offset_start = '00000000'

    while True:
        try:
            inst = xed.decode()
        except :
            inst = 'invalid instruction \n'

        if inst is None:
            break;

        if inst != 'invalid instruction \n':
            string += inst.dump_intel_format() + '\n'

    return string


def main():
    hex_string = openFile('program.exe')
    length = len(hex_string)
    
    original_string = decode(hex_string, 0x0)
    lines_original = original_string.split('\n')

    output1 = open('output1.txt', 'w')

    #check every 500 lines for 20 times
    break_lines = []
    break_recover = []

    break_point = 500
    for k in range(0, 20):
        break_point_hex = '0x' + str(break_point)
        break_point_int = int(break_point_hex, 0)
        string_break_point = hex_string[break_point_int:]

        #output the break point line number
        output1.write('break point line number: ' + break_point_hex + ', ')
        break_lines.append(break_point_hex)
        break_string = decode(string_break_point, break_point_int)

        lines_break_point = break_string.split('\n')
        i = len(lines_original) - 1
        j = len(lines_break_point) - 1
        while (i > 0 or j > 0):
            if (lines_original[i] != lines_break_point[j]):
                # print(lines_break_point[j] + ' ')
                break;
            i -= 1
            j -= 1
        #output the number of lines takes for recovery
        output1.write('lines take to recover: ' + str(j+1) + '\n')
        break_recover.append(j+1)
        break_point += 500


    output2 = open('output2.txt', 'w')
    #take random break point for 20 times
    #the random integer is selected from 0 to 3/4 of the program

    random_lines = []
    random_recover = []
    quarter_break = length * 3 / 4
    for k in range(0, 20):
        random_point_int = getRanInt(quarter_break)
        random_point_hex = '0x' + str(random_point_int)
        random_point_int = int(random_point_hex, 0)
        string_random_point = hex_string[random_point_int:]

        #output the break point line number
        output2.write('break point line number: ' + random_point_hex + ', ')
 
        random_lines.append(random_point_hex)
        random_string = decode(string_random_point, random_point_int)

        lines_random_point = random_string.split('\n')
        i = len(lines_original) - 2
        j = len(lines_random_point) - 2
        while (i > 0 or j > 0):
            if (lines_original[i] != lines_random_point[j]):
                # print(lines_random_point[j])
                break;
            i -= 1
            j -= 1
        #output the number of lines takes for recovery
        output2.write('lines take to recover: ' + str(j+1) + '\n')
        random_recover.append(j+1)

    
main()