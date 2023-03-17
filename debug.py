import matplotlib.pyplot as plt
import math


def ra_f(freq):
    numerator = (12194 ** 2) * (freq ** 4)
    denominator1 = (freq ** 2 + 20.6 ** 2)
    denominator2 = ((freq ** 2 + 107.7 ** 2) * (freq ** 2 + 737.9 ** 2)) ** 0.5
    denominator3 = (freq ** 2 + 12194 ** 2)
    ra = numerator / (denominator1 * denominator2 * denominator3)
    return ra


def a_f(freq):
    a = 20 * math.log(ra_f(freq), 10) + 2
    return a


def rb_f(freq):
    numerator = (12194 ** 2) * (freq ** 3)
    denominator1 = (freq ** 2 + 20.6 ** 2)
    denominator2 = ((freq ** 2 + 158.5 ** 2)) ** 0.5
    denominator3 = (freq ** 2 + 12194 ** 2)
    rb = numerator / (denominator1 * denominator2 * denominator3)
    return rb


def b_f(freq):
    b = 20 * math.log(rb_f(freq), 10) + 0.17
    return b


def rc_f(freq):
    numerator = (12194 ** 2) * (freq ** 2)
    denominator1 = (freq ** 2 + 20.6 ** 2)
    denominator2 = (freq ** 2 + 12194 ** 2)
    rc = numerator / (denominator1 * denominator2)
    return rc


def c_f(freq):
    c = 20 * math.log(rc_f(freq), 10) + 0.06
    return c


def rd_f(freq):
    h = ((1037918.48 - freq ** 2) ** 2 + 1080768.16 * (freq ** 2)) / (
                (9837328 - freq ** 2) ** 2 + 11723776 * (freq ** 2))
    rd = (freq / (6.8966888496476 * 10 ** -5)) * (h / (freq ** 2 + 79919029) * (freq ** 2 + 1345600)) ** 0.5
    return rd


def d_f(freq):
    d = 20 * math.log(rd_f(freq), 10)
    return d


freq_in = list(range(20, 20000, 1))

ra_out = [ra_f(i) for i in freq_in]
# plt.plot(freq_in, ra_out)

a_out = [a_f(i) for i in freq_in]
plt.xscale("log")
# plt.plot(freq_in, a_out)

b_out = [b_f(i) for i in freq_in]
plt.xscale("log")
# plt.plot(freq_in, b_out)

c_out = [c_f(i) for i in freq_in]
plt.xscale("log")
# plt.plot(freq_in, c_out)

d_out = [d_f(i) for i in freq_in]
plt.xscale("log")
plt.plot(freq_in, d_out)

plt.show()
