filepath = r'..\data\lvtemporary_813804.tmp.csv'
with open(filepath, 'r') as fo:
    ''' read file and skip first 2 lines '''
    fo_read_list = fo.readlines()[1:]

fo_read_list = [i.rstrip('\n') for i in fo_read_list]       # remove '\n' for lines

ampl_list = [float(i.split(',')[1]) for i in fo_read_list]  # withdraw amplitude
# print(ampl_list)

peaks = []
for i in range(len(ampl_list) - 4):
    ''' select 5 points at a time. If the location of max value is in the middle of selected points, then it's a peak. '''
    values = ampl_list[i:i+5]               # select 5 points for comparison at a time
    max_value = max(values)                 # find max
    if values.index(max_value) == 2:        # append qualified peak
        peaks.append((max_value, i+2))
peaks.sort(reverse=True)
print(sorted((peaks), reverse=True))
[print(f'ampl = {i[0]:>8.3f}, index = {i[1]:>3}') for i in peaks]


# peaks = []
# compare_len = 9                                 # specify select points. (odd value only)
# index_mid = int((compare_len - 1 ) / 2)         # index of the middle point.
# for i in range(len(ampl_list) - compare_len):
    # values = ampl_list[i:i+compare_len]         # select n points for comparision at a time
    # max_value = max(values)                     # find max
    # if values.index(max_value) == index_mid:    # append qualified peak
        # peaks.append((ampl_list[i+index_mid], i+index_mid))
# print(sorted((peaks), reverse=True))