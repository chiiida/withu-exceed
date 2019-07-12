const baseURL = 'https://exceed.superposition.pknn.dev';

let mainData = {
	"data": {
        "msg": "",
        "bpm" : [],
        "vibration": []
	}
}

function getDocMsg() {
    mainData.data.msg = $('#docMsg').val()

    return mainData
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


// POST
function postMsg() {
    fetch(baseURL + '/data/withu', {
        method: 'PUT',
        body: JSON.stringify(getDocMsg()),
        headers:{
          'Content-Type': 'application/json'
        }
      }).then(res => res.json())
      .then(response => console.log('Success:', JSON.stringify(response)))
      .catch(error => console.error('Error:', error));
}

