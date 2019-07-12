from machine import Pin, ADC
from time import sleep, sleep_us
import json
import urequests as requests
from _thread import start_new_thread as thread
import network
import gc

gc.enable()

#  Setup
EXITALL = False

p_vibration = Pin(27, Pin.IN)
p_RLED = Pin(14, Pin.OUT)
p_GLED = Pin(12, Pin.OUT)
p_BLED = Pin(13, Pin.OUT)  # Pin led !!!
p_buzzer = Pin(5, Pin.OUT)
p_buzzer2 = Pin(18, Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
hr = ADC(Pin(34))
hr.atten(ADC.ATTN_11DB)
hr.width(ADC.WIDTH_12BIT)
API_alert = "https://exceed.superposition.pknn.dev/data/withu"
API_data = "http://103.86.50.95:5000/data"

#  Init Status
LEDSTATUS = 'disconnected'
WIFISTATUS = False
VIBRATIONSTATUS = False
HEARTRATESTATUS = False
ALERTSTATUS = False
MSGALERT = False

#  Connecting WIFI


def WIFIConnect():
    global WIFISTATUS, LEDSTATUS, wlan, EXITALL, p_RLED, p_GLED, p_BLED
    WIFISTATUS = False
    wlan.connect('exceed16_8', '12345678')
    print('connecting')
    p_RLED.value(1)
    LEDSTATUS = 'connecting'
    while not wlan.isconnected():
        p_RLED.value(0)
        sleep(0.01)
    WIFISTATUS = True
    print('connected')
    p_RLED.value(0)
    p_GLED.value(1)


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
        p_RLED.value(0)
        p_GLED.value(0)
        p_BLED.value(1)
        count = 0
        v_count = 0
        while not (HEARTRATESTATUS):
            count += 1
            if (p_vibration == 0):
                v_count += 1
            sleep(0.01)
        if (v_count >= (count * 20 / 100)):
            vibration = True
        else:
            vibration = False
        VIBRATIONSTATUS = True
        sleep(0.01)


#  Read HR
def readHR():
    time = 10  # in seconds.
    sleep_time = 0.01

    data_len = int(time//sleep_time)
    data = [100 for _ in range(data_len)]
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

    n_beat = 0

    for i, res in enumerate(data):
        if i == 0:
            continue
        if res > thres and not data[i-1] > thres:
            n_beat += 1

    del data
    gc.collect()
    bpm = n_beat*60//time
    return bpm


#  Recive data from readHR
def HeartRate():
    global HEARTRATESTATUS, bpm, EXITALL, LEDSTATUS, p_RLED, p_GLED, p_BLED
    while not EXITALL:
        p_RLED.value(0)
        p_GLED.value(0)
        p_BLED.value(1)
        bpm = 0
        for i in range(2):
            bpm += readHR()
        bpm /= 2
        HEARTRATESTATUS = True
        print('HEARTRATESTATUS = ', HEARTRATESTATUS)
        sleep(0.1)


# LED tell status
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
    global API_data, HEARTRATESTATUS, bpm, VIBRATIONSTATUS, vibration, EXITALL
    while not EXITALL:
        if (VIBRATIONSTATUS and HEARTRATESTATUS):
            if WIFISTATUS:
                data = json.dumps({
                    'data': {
                        'vibration': vibration,
                        'bpm': bpm
                    }
                })
                print(data)
                headers = {'Content-type': 'application/json'}
                VIBRATIONSTATUS = False
                HEARTRATESTATUS = False
                print(requests.post(API_data, data=data, headers=headers).content)
                gc.collect()
        sleep(5)

#  get alert from web


def getAlert():
    global API_alert, ALERTSTATUS, MSGALERT
    alerted = False
    msgAlerted = False
    while not EXITALL:
        if WIFISTATUS:
            headers = {'Content-type': 'application/json'}
            rest = requests.get(API_alert, headers=headers).json()
            ALERTSTATUS = rest["alert"]
            if type(ALERTSTATUS) != bool:
                ALERTSTATUS = ALERTSTATUS.lower() == 'true'
            MSGALERT = rest["msg"] != ''
            if ALERTSTATUS and not alerted:
                for _ in range(10):
                    print('Alert mode!!!!!!')
                    p_buzzer.value(1)
                    sleep(0.2)
                    p_buzzer.value(0)
                    sleep(0.8)
                alerted = True
            elif not ALERTSTATUS:
                alerted = False
            if MSGALERT and not msgAlerted:
                for _ in range(5):
                    print('msgAlert!!!!!!')
                    p_buzzer2.value(1)
                    sleep(0.05)
                    p_buzzer2.value(0)
                    sleep(0.05)
                msgAlerted = True
            elif not MSGALERT:
                msgAlerted = False
        gc.collect()
        sleep(1)


#  Buzzer beep when alert
def alertMode():
    global ALERTSTATUS
    count = 0
    while not EXITALL:
        if ALERTSTATUS and count < 10:
            print('Alert mode!!!!!!')
            p_buzzer.value(1)
            sleep(0.5)
            p_buzzer.value(0)
            sleep(0.5)
            count += 1
        else:
            if not ALERTSTATUS:
                count = 0
            sleep(3)

#  Buzzer beep when receivemsg


def msgalertMode():
    global MSGALERT
    count = 0
    while not EXITALL:
        if MSGALERT and count < 3:
            print('msgAlert!!!!!!')
            p_buzzer2.value(1)
            sleep(1)
            p_buzzer2.value(0)
            sleep(0.1)
            p_buzzer2.value(1)
            sleep(0.1)
            p_buzzer2.value(0)
            sleep(0.1)
            p_buzzer2.value(1)
            sleep(0.1)
            p_buzzer2.value(0)
            sleep(0.1)
            p_buzzer2.value(1)
            sleep(0.1)
            p_buzzer2.value(0)
            sleep(2)
            count += 1
        else:
            if not MSGALERT:
                count = 0
            sleep(3)


#  Main Begins here
WIFIConnect()
thread(vibrationSensor, [])
thread(HeartRate, [])  # Pass
thread(postData, [])  # Pass
thread(WIFICheck, [])
# thread(statusLED, [])
thread(getAlert, [])
# thread(alertMode, [])
# thread(msgalertMode, [])
try:
    while True:
        sleep(0.0005)
except:
    EXITALL = True
