filepath = r'.\data\lvtemporary_813804.tmp.csv'
with open(filepath, 'r') as fo:
    ''' read file and skip first row (column header) '''
    fo_read_lines = fo.readlines()[1:]

fo_read_lines = [i.rstrip('\n') for i in fo_read_lines]       # remove '\n' for lines

''' Fixed points'''
peaks = []
for i in range(len(fo_read_lines) - 4):
    ''' select 5 amplitudes at a time. If the index of max value is in the middle of selected points in both reverse and non-reverse list, then it's a peak. '''
    frequencies = []
    amplitudes = []
    for line in fo_read_lines[i:i+5]:
        ''' select 5 points for comparison at a time '''
        freq, ampl = line.split(',')
        frequencies.append(float(freq))
        amplitudes.append(float(ampl))

    ampl_max = max(amplitudes)                      # find max
    amplitudes_rev = list(reversed(amplitudes))     # reverse amplitudes
    if amplitudes.index(ampl_max) == 2 and amplitudes_rev.index(ampl_max) == 2:        # append qualified peak
        ''' max value must located in both reversed and non-reversed list '''
        peaks.append((amplitudes[2], frequencies[2], i+2))
peaks.sort(reverse=True)
print(f'Find {len(peaks)} peaks.')
[print(f'ampl = {p[0]:>9.4f}, freq = {p[1]:>8.2f}, index= {p[2]:>4}') for p in peaks]


''' Variable points '''
# peaks = []
# select_len = 5                                  # specify select points. (odd value only)
# index_mid = int((select_len - 1) / 2)           # index of the middle point.
# for i in range(len(fo_read_lines) - select_len - 1):
#     ''' select n amplitudes at a time. If the index of max value is in the middle of selected points in both reverse and non-reverse list, then it's a peak. '''
#     frequencies = []
#     amplitudes = []
#     for line in fo_read_lines[i:i+select_len]:
#         ''' select n points for comparison at a time '''
#         freq, ampl = line.split(',')
#         frequencies.append(float(freq))
#         amplitudes.append(float(ampl))
#     ampl_max = max(amplitudes)                      # find max
#     amplitudes_rev = list(reversed(amplitudes))     # reverse amplitudes
#     if amplitudes.index(ampl_max) == index_mid and amplitudes_rev.index(ampl_max) == index_mid:        # append qualified peak
#         ''' max value must located in both reversed and non-reversed list '''
#         peaks.append((amplitudes[index_mid], frequencies[index_mid], i+index_mid))
# peaks.sort(reverse=True)
# print(f'Find {len(peaks)} peaks.')
# [print(f'ampl = {p[0]:>9.4f}, freq = {p[1]:>8.2f}, index= {p[2]:>4}') for p in peaks]