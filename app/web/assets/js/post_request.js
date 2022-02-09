var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: []
        }]
    },

    // Configuration options go here
    options: {
      responsive: true
      // maintainAspectRatio: false
    }
});


setInterval(change_label, 1000);
// change_label();

function change_label(){
  console.log();
  //Create xhttp object
  var xhttp = new XMLHttpRequest();
  //Listen for the response of your xhttp object
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      //If the request is 200 aka succesfull, set the text of the label to the response text of the xhttp request
      console.log(this.responseText);


      var today = new Date();

      addData(chart, today.getSeconds(), parseFloat(this.responseText))

      document.getElementById("Label").innerHTML = this.responseText;
    }
  };
  //Open a post request with the xhttp object. 
  xhttp.open("POST", "http://127.0.0.1:5000/change_label", true);
  // Send the post request
  xhttp.send();
}



function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}