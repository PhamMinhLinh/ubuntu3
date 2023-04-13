var temperature = document.getElementById('temperature');
var apikey = document.getElementById('apikey').value ;
var devicename = "Dec12012";

function getdevice(){
    var requests = $.get('/api/' + apikey + '/deviceinfo/' + devicename);
    
    var tm = requests.done(function (result){
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        addData(temp_chart, time, result[3]);
        document.getElementById("card-temp").innerHTML = result[3];
        document.getElementById("card-humidity").innerHTML = result[4];
        if (couter >= 10 ){
            removeData(temp_chart);
        }
        couter++;

        setTimeout(getdevice, 2000);
        
    
    });
    
}

//temperature chart object created 
var temp_chart = new Chart(temperature, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Accident Warning System - Real Time',
            data: [],
            fill:true,
            backgroundColor: 'rgba(244, 67, 54, 0.1)',
            borderColor:'rgba(244, 67, 54, 1)',
            borderWidth: 3
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});


function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
    chart.update();
}

var couter = 0; 

getdevice();
