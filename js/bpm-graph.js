const myURL = 'https://exceed.superposition.pknn.dev';

function drawGraph() {
    fetch(myURL + '/data/withu/timestamp')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      var timestamp = myJson.map(function(v) { return v.slice(10, 16) });
      var lineReal = document.getElementById('real-time').getContext('2d');
      
      fetch(myURL + '/data/withu/bpm')
        .then(function(response) {
        return response.json();
        })
        .then(function(myJson) {
            var chart = new Chart(lineReal, {
                // The type of chart we want to create
                type: 'line',
            
                // The data for our dataset
                data: {
                    labels: timestamp,
                    datasets: [{
                        label: 'Real-time BPM',
                        borderColor: 'rgb(255, 99, 132)',
                        data: myJson,
                        backgroundColor: 'rgba(0, 0, 0, 0)',
                    }]
                },
            
                // Configuration options go here
                options: {
                    scales: {
                        yAxes:[{
                            ticks: {
                                min: myJson[0] - 20,
                                max: myJson.lenght + 20
                                // stacked: true
                            }
                        }],
                    }
                }
            });
        });
  });
}

function putPulse(bpm) {
    document.getElementById('pulse').innerHTML = bpm
}

drawGraph()

setInterval(() => {
    drawGraph()
}, 60000)