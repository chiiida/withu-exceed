from machine import Pin, ADC
from time import sleep, sleep_us
import json
import urequests as requests
from _thread import start_new_thread as thread
import network


#  Import Statistic
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
#  Import Statistic End here


#  Setup
EXITALL = False

p_vibration = Pin(27, Pin.IN)
p_RLED = Pin(14, Pin.OUT)
p_GLED = Pin(12, Pin.OUT)
p_BLED = Pin(13, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
hr = ADC(Pin(34))
hr.atten(ADC.ATTN_11DB)
hr.width(ADC.WIDTH_12BIT)
#API = "https://exceed.superposition.pknn.dev/data/withu"
API = "http://10.46.75.118:5000/data"

#  Init Status
LEDSTATUS = 'disconnected'
WIFISTATUS = False
VIBRATIONSTATUS = False
HEARTRATESTATUS = False


#  Connecting WIFI
def WIFIConnect():
    global WIFISTATUS, LEDSTATUS, wlan, EXITALL
    WIFISTATUS = False
    wlan.connect('exceed16_8', '12345678')
    print('connecting')
    LEDSTATUS = 'connecting'
    while not wlan.isconnected():
        sleep(0.01)
    WIFISTATUS = True
    print('connected')
    LEDSTATUS = 'connected'


#  Checking WIFI
def WIFICheck():
    global LEDSTATUS, EXITALL
    while not EXITALL:
        if not wlan.isconnected():
            LEDSTATUS = 'disconnected'
            WIFIConnect()
        sleep(2)


#  Vibration Detect
def vibrationSensor():
    global VIBRATIONSTATUS, vibration, EXITALL, LEDSTATUS
    while not EXITALL:
        LEDSTATUS = 'measuring'
        count = 0
        for i in range(6000):
            if (p_vibration == 0):
                count += 1
            sleep(0.01)
        if (count >= 5000):
            vibration = True
        else:
            vibration = False
        VIBRATIONSTATUS = True
        print('VIBRATIONSTATUS = ', VIBRATIONSTATUS)
        sleep(0.01)


#  Read HR
def readHR():
    time = 10  # in seconds.
    sleep_time = 0.01
    
    data = []
    data_len = time//sleep_time
    while not EXITALL:
        data.append(100)
        if len(data) == data_len:
            break

    i = 0
    sum_data = 0
    print("Start measuring")
    while i < data_len:
        data[i] = hr.read()
        sum_data += data[i]
        # print(data[i])
        i += 1
        sleep(sleep_time)
    print("finished")

    average = sum_data/data_len
    thres = average*10

    result = [raw > thres for raw in data]
    del data

    n_beat = 0

    for i, res in enumerate(result):
        if i == 0:
            continue
        if res and not result[i-1]:
            n_beat += 1
    del result

    bpm = n_beat*60//time
    return bpm


#  Recive data from readHR
def HeartRate():
    global HEARTRATESTATUS, bpm, EXITALL, LEDSTATUS
    while not EXITALL:
        LEDSTATUS == 'measuring'
        bpm = readHR()
        HEARTRATESTATUS = True
        print('HEARTRATESTATUS = ', HEARTRATESTATUS)


# In progress
def statusLED():
    while not EXITALL:
        if (LEDSTATUS == 'disconnected'):
            p_RLED.value(1)
            p_GLED.value(0)
            p_BLED.value(0)
        elif (LEDSTATUS == 'connecting'):
            p_RLED.value(1)
            p_GLED.value(0)
            p_BLED.value(0)
            sleep(0.01)
            p_RLED.value(0)
            p_GLED.value(0)
            p_BLED.value(0)
        elif (LEDSTATUS == 'measuring'):
            p_RLED.value(0)
            p_GLED.value(0)
            p_BLED.value(1)
            sleep(0.01)
            p_RLED.value(0)
            p_GLED.value(0)
            p_BLED.value(0)
        else:
            p_RLED.value(0)
            p_GLED.value(1)
            p_BLED.value(0)
    sleep(0.01)



#  Send data to web
def postData():
    global API, HEARTRATESTATUS, bpm, VIBRATIONSTATUS, vibration, EXITALL
    while not EXITALL:
        if (VIBRATIONSTATUS and HEARTRATESTATUS):
            if WIFISTATUS:
                data = json.dumps({
                    'data':{
                        'vibration': vibration,
                        'bpm': bpm
                    }
                })
                print(data)
                headers = {'Content-type': 'application/json'}
                VIBRATIONSTATUS = False
                HEARTRATESTATUS = False
                print(requests.post(API, data=data, headers=headers).content)
        sleep(5)


#  Main Begins here
WIFIConnect()
thread(vibrationSensor, [])
thread(HeartRate, [])
thread(postData, [])
#thread(WIFICheck(), [])
#thread(statusLED(), [])
try:
    while True:
        sleep(0.0005)
except:
    EXITALL = True