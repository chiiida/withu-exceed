const baseURL = 'https://exceed.superposition.pknn.dev';

// GET
fetch(baseURL + '/data/withu')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      $('#readDocMsg').append(myJson.msg)
  });