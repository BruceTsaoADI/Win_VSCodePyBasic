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


while True:
    hexin = input('\nEnter hex value: ')
    if hexin.startswith('0x'):
        hexin = hexin[2:]
    check = [c.lower() in DICT_HEX2BIN for c in hexin]
    if False in check:
        print('Please enter legal hex value. 0~9, A, B, C, D, E. (capital insensitive)')
    else:
        binout = ''
        for h in hexin.lower():
            binout += DICT_HEX2BIN[h] + '-'
        print(binout[:-1])
