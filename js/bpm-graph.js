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
            console.log(Math.max(...myJson))
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
                        yAxes: [{
                            display: true,
                            ticks: {
                                max: Math.max(...myJson) + 5,
                                min: Math.min(...myJson) - 5,
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Heart rate',
                            }
                        }],
                        xAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Minutes',
                            }
                        }]
                    },
                }
            });
        });
  });
}

function drawGraphBar() {
    fetch(myURL + '/data/withu/timestamp')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
      var timestamp = myJson.map(function(v) { return v.slice(10, 16) });
      var lineReal = document.getElementById('vibration').getContext('2d');
      
      fetch(myURL + '/data/withu/vibration')
        .then(function(response) {
        return response.json();
        })
        .then(function(myJson) {
            var chart = new Chart(lineReal, {
                type: 'bar',
                data: {
                    labels: timestamp,
                    datasets: [{
                        label: 'Real-time Vibration',
                        backgroundColor: 'rgba(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: myJson
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            display: true,
                            ticks: {
                                max: Math.max(...myJson) + 5,
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Vibration',
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Minutes',
                            }
                        }]
                    },
                }
            });
        });
  });
}

function putPulse(bpm) {
    document.getElementById('pulse').innerHTML = bpm
}

drawGraph()
drawGraphBar()

setInterval(() => {
    drawGraph()
    drawGraphBar()
}, 60000)