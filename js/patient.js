const baseURL = 'https://exceed.superposition.pknn.dev';

// GET
function getMsg() {
    fetch(baseURL + '/data/withu')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      document.getElementById("readDocMsg").innerHTML = myJson.msg;
    // $('#readDocMsg').append(myJson.msg)
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

img = document.getElementById('animated')

function pulseAnimated() {
  img.innerHTML = '<img src="img/1.png">';
  setTimeout(() => img.innerHTML = '<img src="img/2.png">', 500);
}

setInterval(() => {
    getMsg()
    pulseAnimated()
}, 1000)