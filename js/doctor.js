const baseURL = 'https://exceed.superposition.pknn.dev';

let mainData = {
	"data": {
        "msg": "",
        "bpm" : [],
        "vibration": [],
        "alert": false
	}
}

function getDocMsg() {
    msg = $('#docMsg').val()
    msgVal = {
        "value" : msg
    }
    document.getElementById('docMsg').value = '';

    return msgVal
}

// POST
function postAllData() {
    fetch(baseURL + '/data/withu', {
        method: 'POST',
        body: JSON.stringify(getDocMsg()),
        headers:{
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:', error));
}

// PUT
function postMsg() {
    fetch(baseURL + '/data/withu/msg', {
        method: 'PUT',
        body: JSON.stringify(getDocMsg()),
        headers:{
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:', error));
}

