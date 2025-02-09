DICT_HEX2BIN = {
            '0': '0000',
            '1': '0001',
            '2': '0010',
            '3': '0011',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'a': '1010',
            'b': '1011',
            'c': '1100',
            'd': '1101',
            'e': '1110',
            'f': '1111',
        }


def hex_to_bin(hexin):
    binout = ''
    for h in hexin.lower():
        binout += DICT_HEX2BIN[h] + '-'
    print(binout[:-1])
        
    binout_nodash = binout.replace('-', '')
    str_bit = f'{"Bit":<7}'
    len_bit = len(binout_nodash)
    for i in range(len(binout_nodash)):
        str_bit += f'{len_bit-1-i:^3}'
    print(str_bit)
    
    str_val = f'{"Value":<7}'
    for i in range(len(binout_nodash)):
        str_val += f'{binout_nodash[i]:^3}'
    print(str_val)


while True:
    hexin = input('\nEnter hex value ("q" to quit): ')
    if hexin.lower() == 'q':
        exit()
        
    if hexin.startswith('0x'):
        hexin = hexin[2:]
    check = [c.lower() in DICT_HEX2BIN for c in hexin]
    
    if False in check:
        print('Please enter legal hex value. 0~9, A, B, C, D, E. (capital insensitive)')
    else:
        hex_to_bin(hexin)
















