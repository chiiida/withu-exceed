const mainURL = 'https://exceed.superposition.pknn.dev';

function putAlert(status) {
  fetch(mainURL + '/data/withu/alert', {
      method: 'PUT',
      body: JSON.stringify({
          "value" : status
      }),
      headers:{
        'Content-Type': 'application/json'
      }
    }).then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error));
}

function getBpm() {
    fetch(mainURL + '/data/withu/bpm')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      document.getElementById('pulse').innerText = myJson.slice(-1);
  });
}

function alertProb() {
  fetch(mainURL + '/data/withu/bpm')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    var bpm = myJson;

    fetch(mainURL + '/data/withu/vibration')
    .then(function(response) {
      return response.json();
    })
    .then(function(myJson) {
      var vibration = myJson;

      for (var i = 0; i < vibration.lenght; i++) {
        if (bpm[i] > 100 && vibration[i] < 30) {
          putAlert(true)
          setTimeout(() => putAlert(false), 10000);
        }
      }
    });
  });
}

setInterval(() => {
  getBpm();
  alertProb();
}, 1000)
