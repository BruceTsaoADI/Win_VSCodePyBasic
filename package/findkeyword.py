import os

path_dir = r'C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\06_MCU\Maxim\Project\EVK_32670\20231212_ADV7671A\ARM\ADV7671A'
#path_dir = r'C:/Users/btsao/OneDrive - Analog Devices, Inc/Documents/BruceTsao/06_MCU/STM/Project/STM32F446VET6/ADV7671A/Driver_ADV7671A/'
filters = ['s_obj_list_inst']

print('\n'*2)
print('*'*20 + str(filters) + '*'*20 + '\n')

c_headers = []
c_files = []
c_path_files = []
for root, dirs, files in os.walk(path_dir):
    for file in files:
        ''' collect filtered files '''
        if file.endswith('.h'):
            c_headers.append(file)
            c_path_files.append(os.path.join(root, file))
        elif file.endswith('.c'):
            c_files.append(file)
            c_path_files.append(os.path.join(root, file))

num_result = 0
for path in c_path_files:
    with open(path, 'r') as fo:
        lines = fo.readlines()
        index_line = 1
        for line in lines:
            for filter in filters:
                if filter in line:
                    num_result += 1
                    print(f'{path}({index_line})'  )
                    print(line)
            index_line += 1

print(f'Find {num_result} results.')



