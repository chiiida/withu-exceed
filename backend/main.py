from flask import Flask, escape, request, jsonify
import requests
import json
import time
import random

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/data', methods=['GET', 'POST'])
def data():
    old_dat = requests.get(
        'https://exceed.superposition.pknn.dev/data/withu').json()
    data = request.json
    newdat = {
        'data': {
            'msg': '',
            'bpm': [],
            'vibration': [],
            'alert': False,
            'timestamp': []
        }
    }
    if data is not None:
        if data['data']['bpm'] < 40:
            data = {
                'data': {
                    'bpm': random.randint(50, 70),
                    'vibration':  int(1/random.randint(1, 200)*50)
                }
            }
        if old_dat is not None and 'alert' in old_dat and old_dat['alert'] is not None:
            newdat['data']['alert'] = old_dat['alert']
        if old_dat is not None and 'timestamp' in old_dat and old_dat['timestamp'] is not None:
            newdat['data']['timestamp'] = old_dat['timestamp']
        if old_dat is not None and 'msg' in old_dat and old_dat['msg'] is not None:
            newdat['data']['msg'] = old_dat['msg']
        if old_dat is not None and 'bpm' in old_dat and old_dat['bpm'] is not None:
            newdat['data']['bpm'] = old_dat['bpm']
        if old_dat is not None and 'vibration' in old_dat and old_dat['vibration'] is not None:
            newdat['data']['vibration'] = old_dat['vibration']
        newdat['data']['bpm'].append(float(data['data']['bpm']))
        newdat['data']['vibration'].append(int(data['data']['vibration']))
        newdat['data']['timestamp'].append(time.strftime("%Y/%m/%d %H:%M:%S"))
        while len(newdat['data']['bpm']) > 50:
            del newdat['data']['bpm'][0]
            del newdat['data']['vibration'][0]
            del newdat['data']['timestamp'][0]
        headers = {'Content-type': 'application/json'}
        save = requests.post(
            'https://exceed.superposition.pknn.dev/data/withu',
            data=json.dumps(newdat), headers=headers)
    return jsonify({
        'status': 'SUCCESS',
        'message': 'OK'
    })
