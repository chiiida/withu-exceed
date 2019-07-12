const myURL = 'https://exceed.superposition.pknn.dev';

function getBpm() {
    fetch(myURL + '/data/withu/bpm')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      document.getElementById('pulse').innerText = myJson.slice(-1);
  });
}

getBpm();