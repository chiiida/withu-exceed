from flask import Flask, escape, request, jsonify
import requests
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
        'msg': '',
        'bpm': [],
        'vibration': []
    }
    if data is not None:
        if old_dat['msg'] is not None:
            newdat['msg'] = old_dat['msg']
        if old_dat['bpm'] is not None:
            newdat['bpm'] = old_dat['bpm']
        if old_dat['vibration'] is not None:
            newdat['vibration'] = old_dat['vibration']
        newdat['bpm'].append(float(data['data']['bpm']))
        newdat['vibration'].append(int(data['data']['vibration']))
        requests.post(
            'https://exceed.superposition.pknn.dev/data/withu', json=old_dat)
    return jsonify({
        'status': True,
        'msg': 'OK'
    })
