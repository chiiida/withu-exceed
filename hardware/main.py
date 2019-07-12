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
API = "https://exceed.superposition.pknn.dev/data/withu"


#  Init Status
LEDSTATUS = 'disconnected'
WIFISTATUS = False
VIBRATIONSTATUS = False
HEARTRATESTATUS = False


#  Connecting WIFI
def WIFIConnect():
    global WIFISTATUS, LEDSTATUS, wlan
    WIFISTATUS = False
    wlan.connect('exceed16_8', '12345678')
    print('connecting')
    while not wlan.isconnected():
        sleep(0.01)
    WIFISTATUS = True
    LEDSTATUS = 'connected'

# In progress !!!


def WIFICheck():
    global LEDSTATUS
    while not EXITALL:
        if not wlan.isconnected():
            LEDSTATUS = 'disconnected'
            WIFIConnect()
        sleep(2)


#  Vibration Detect
def vibrationSensor():
    global VIBRATIONSTATUS, vibration
    while not EXITALL:
        count = 0
        for i in range(60000):
            if (p_vibration == 0):
                count += 1
            sleep(0.001)
        if (count >= 5000):
            vibration = True
        else:
            vibration = False
        VIBRATIONSTATUS = True
        print('VIBRATIONSTATUS out = ', VIBRATIONSTATUS)
        sleep(0.01)


#  Read HR
def readHR():
    time = 10  # in seconds.
    sleep_time = 0.01

    data = []
    while not EXITALL:
        data.append(100)
        if len(data) == time//sleep_time:
            break

    i = 0

    while i < len(data):
        data[i] = hr.read()
        # print(data[i])
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


#  Recive data from readHR
def HeartRate():
    global HEARTRATESTATUS, bpm
    while not EXITALL:
        bpm = readHR()
        HEARTSTATUS = True


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
        else:
            p_RLED.value(0)
            p_GLED.value(1)
            p_BLED.value(0)
    sleep(0.01)


#  Send data to web
def postData():
    global API, HEARTRATESTATUS, bpm, VIBRATIONSTATUS, vibration
    while not EXITALL:
        if (VIBRATIONSTATUS):
            print('VIBRATIONSTATUS in = ', VIBRATIONSTATUS)
            print('begin post')
            Pin(5, Pin.OUT).value(1)
            print('WIFISTATUS =', WIFISTATUS)
            if WIFISTATUS:
                r = requests.get(API)
                json_data = r.json()
                data = json.dumps({
                    'vibration': vibration,
                    'bpm': bpm
                })
                print(data)
                headers = {'Content-type': 'application/json'}
                print(requests.post(API, data=data, headers=headers).content)
                VIBRATIONSTATUS = False
                HEARTRATESTATUS = False
        sleep(0.01)


#  Main Begins here
WIFIConnect()
# thread(WIFICheck(), []) # In progress
# thread(statusLED(), []) # In progress
thread(vibrationSensor, [])
thread(HeartRate, [])
thread(postData, [])

try:
    while True:
        sleep_us(10)
except:
    EXITALL = True
