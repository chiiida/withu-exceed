from machine import Pin, ADC
from time import sleep


def mean(data):
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n


def _ss(data):
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss


def stddev(data, ddof=0):
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5


hr = ADC(Pin(34))
hr.atten(ADC.ATTN_11DB)
hr.width(ADC.WIDTH_12BIT)


def readHR():
    time = 10  # in seconds.
    sleep_time = 0.01

    data = []
    while True:
        data.append(100)
        if len(data) == time//sleep_time:
            break

    i = 0

    while i < len(data):
        data[i] = hr.read()
        print(data[i])
        i += 1
        sleep(sleep_time)

    average = sum(data)/len(data)
    thres = average+0.75*stddev(data)

    result = [raw > thres for raw in data]

    n_beat = 0

    for i, res in enumerate(result):
        if i == 0:
            continue
        if res and not result[i-1]:
            n_beat += 1

    bpm = n_beat*60//time
    return bpm
