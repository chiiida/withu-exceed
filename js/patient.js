const baseURL = 'https://exceed.superposition.pknn.dev';

// GET
function getDocMsg() {
    fetch(baseURL + '/data/withu')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      $('#readDocMsg').append(myJson.msg)
      console.log(myJson)
  });
}

fetch(baseURL + '/data/withu')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      $('#readDocMsg').append(myJson.msg)
      console.log(myJson)
  });