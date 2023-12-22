import time

def c2py_macro_read(macro: str) -> tuple:
    macro_name = ''
    macro_exp = ''
    segments = macro.split(' ')
    macro_name = segments[1]
    for s in segments[2:]:
        if s.startswith('"'):
            macro_exp = s
            break
        elif s.startswith('0x'):
            macro_exp = int(s, 0)
            break
        elif s.isdigit():
            macro_exp = int(s)
            break
    return macro_name, macro_exp




def c2py_collect_macro(path: str) -> dict:
    ''' To collect all macro in the C or H file and save as Python dictionary.'''
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_macro = {}
    dict_key = ''
    dict_val = ''
    for line in lines:
        line = line.replace('\n', '')
        if line.startswith('#define') and line.find('__') == -1:
            dict_key, dict_val = c2py_macro_read(line)
            dict_macro[dict_key] = dict_val
    return dict_macro


def c2py_collect_array(path: str) -> dict:
    """ To collect all array in the C or H file and save as Python dictionary."""
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_array = {}
    dict_key = ''
    dict_val = []
    array_start = False
    for line in lines:
        if line.startswith('ADI_REG_TYPE'):
            array_name = line.split(' ')[1]
            index_name_end = array_name.find('[')
            dict_key = array_name[:index_name_end]
            dict_val = []
            array_start = True

        if array_start:
            if line.startswith('0x'):
                if line.find(',') == -1:
                    dict_val.append(int(line, 0))
                else:
                    for i in line.split(', '):
                        if i.startswith('0x'):
                            dict_val.append(int(i, 0))
            elif line.startswith('};'):
                array_start = False
                dict_array[dict_key] = dict_val
    return dict_array


def c2py_collect_func(path: str) -> dict:
    """ To collect all array in the C or H file and save as Python dictionary."""
    ''' Exclude #ifndef and #deine pair'''
    with open(path, 'r') as fo:
        lines = fo.readlines()

    dict_func = {}
    dict_key = ''
    dict_val = ''
    func_start = False
    for line in lines:
        # line = line.replace('\n', '')

        if line.startswith('void'):
            func_name = line.split(' ')[1]
            index_name_end = func_name.find('(')
            dict_key = func_name[:index_name_end]
            func_val = []
            func_start = True
            subfun_name = ''
            subfun_devaddr = ''
            subfun_regaddr = ''
            subfun_regbyte = ''
            subfun_regvalue = ''

        if func_start:
            line = line.strip('\t')
            if line.startswith('SIGMA_WRITE_REGISTER_BLOCK'):
                subfun_name = 'SIGMA_WRITE_REGISTER_BLOCK'
                line = line.split('(')[1]
                line = line.split(');')[0]
                argus = line.split(',')
                subfun_devaddr = argus[0].strip()
                subfun_regaddr = argus[1].strip()
                subfun_regbyte = argus[2].strip()
                subfun_regvalue = argus[3].strip()
                func_val.append([subfun_name, subfun_devaddr, subfun_regaddr, subfun_regbyte, subfun_regvalue])
            elif line.startswith('SIGMA_WRITE_DELAY'):
                subfun_name = 'SIGMA_WRITE_DELAY'
                line = line.split('(')[1]
                line = line.split(');')[0]
                argus = line.split(',')
                subfun_devaddr = argus[0].strip()
                subfun_regbyte = argus[1].strip()
                subfun_regvalue = argus[2].strip()
                func_val.append([subfun_name, subfun_devaddr, subfun_regbyte, subfun_regvalue])
            if line.startswith('}'):
                func_start = False
                dict_func[dict_key] = func_val

    return dict_func


file_paths = [
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA_REG.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_SIGMA_PARAM.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST_REG.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST.h',
    r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\08_Python\20230214_Python\data\API_ADAU1787_C\SineTone_IC_1_FAST_PARAM.h',
    ]
c2py_macro = {}
for path in file_paths:
    c2py_macro.update(c2py_collect_macro(path))
# print(c2py_macro)
# print(c2py_macro['R5_MBIAS1_EN_IC_1_Sigma_SHIFT'])

c2py_array = {}
for path in file_paths:
    c2py_array.update(c2py_collect_array(path))
# print(c2py_array)
# print(c2py_array['R1_FDSP_RUN_IC_1_Fast_Default'])

c2py_func = {}
for path in file_paths:
    c2py_func.update(c2py_collect_func(path))
#print(c2py_func)
# print(c2py_func['SEQ_MUTELEFT_download'])


dict_marco_array = {}
dict_marco_array.update(c2py_macro)
dict_marco_array.update(c2py_array)

str = time.time()
print('Start download.')
for f in c2py_func:
    for i in c2py_func[f]:
        func_name = i[0]
        if func_name == 'SIGMA_WRITE_REGISTER_BLOCK':
            dev_addr = dict_marco_array[i[1]]
            reg_addr = dict_marco_array[i[2]]
            reg_byte = dict_marco_array[i[3]]
            reg_value = dict_marco_array[i[4]]
            [print(hex(i)) for i in reg_value if i > 5]
            # print(dev_addr, reg_addr, reg_byte, reg_value)
            # gmsl_reg_write(I2C_BUS_01, dev_addr, reg_addr, reg_value)

        if func_name == 'SIGMA_WRITE_DELAY':
            dev_addr = dict_marco_array[i[1]]
            reg_byte = dict_marco_array[i[2]]
            reg_value = dict_marco_array[i[3]]

            delay_ms = 0
            for i in range(reg_byte):
                delay_ms = (delay_ms << 8) + reg_value[i]
            time.sleep(delay_ms/1000)
            print(f'Delay {delay_ms} ms')
print('End download.')
print(f'Elapse: {time.time() - str}')