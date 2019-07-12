const baseURL = 'https://exceed.superposition.pknn.dev';

// GET
function getMsg() {
    fetch(baseURL + '/data/withu')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      document.getElementById("readDocMsg") = myJson.msg;
    //   $('#readDocMsg').append(myJson.msg)
  });
}

function getBpm() {
    fetch(myURL + '/data/withu/bpm')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      console.log(myJson)
  });
}

function getVibration() {
    fetch(myURL + '/data/withu/vibration')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      console.log(myJson)
  });
}

setInterval(() => {
    getMsg()
}, 1000)