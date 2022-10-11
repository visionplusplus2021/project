$(document).ready(function () {

  var ctx1 = document.getElementById('myChart1').getContext('2d');
  var chart1 = new Chart(ctx1, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      labels: ['Trespasser'],
      datasets: [{
        label: ['count'],
        fill: false,
        backgroundColor: [
          randomColor()
        ],
        // borderColor: 'rgb(255, 99, 132)',
        data: []
      }]
    },
    // Configuration options go here
    options: {
      responsive: true,
      legend: { display: false },
      title: {
        display: false
        // text: 'Vehicle Counting'
      },
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            // suggestedMax: 3000,
            beginAtZero: true
          }
        }]
      }
      // maintainAspectRatio: false
    }
  });

  function listOfColors(len) {
    listOfColorsArray = [];
    for (var i = 0; i < len; i++) {
      listOfColorsArray[i] = randomColor();
    }
    // console.log(listOfColorsArray);
    return listOfColorsArray;
  }
  function randomColor() {
    color = 'rgb(' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ',' + Math.round(Math.random() * 255) + ')';
    return color;
  }
  function updateBarChart(chart, countData) {
    chart.data.datasets.forEach(function (dataset) {
      dataset.data = countData;
    })
    chart.update();
  }

  // ********************** end chart ******************************************
  var csvData = '';

  $('#inputServer').change(function () {
    var data = $(this).find('option:selected').val();
    console.log(data);
    $.ajax({
      type: 'GET',
      url: database_url + "/trespassing_boundary/get_area/" + data,
      success: function (data) {
        var temp1 = [];
        temp1.push("</div><option value=All Areas' >All Areas</option></div>")
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element._id.$oid + ">" + element.area_name + "</option></div>");
        });
        $('#inputLane').html(temp1);
      }
    });
  });

  $('#applyFilter').on('click', function () {
    var startDate = document.getElementById("startDateTimeInput").value;
    var endDate = document.getElementById("endDateTimeInput").value; 

    // var startTimestamp = startDate.getTime();
    // var endTimestamp = endDate.getTime();

    var camera_id = $("#inputServer").find('option:selected').val();
    var camera_name = $("#inputServer").find('option:selected').text();
    var lane = $("#inputLane").find('option:selected').text();

    const data = {
      'start_date': startDate,
      'end_date': endDate,
      'camera_id': camera_id,
      'camera_name': camera_name,
      'area_name': lane
    };
    // console.log(data);

    $.ajax({
      type: 'POST',
      url: database_url+'/trespassing_report/get_by_filter',
      data: data,
      dataType: "text",
      success: function (data) {
        data = JSON.parse(data)

        var count_object = { 'trespasser': 0}
        var count_array = [0];

        var arrayLength = data.length;
        for (var i = 0; i < arrayLength; i++) {
          var dic = data[i];
          class_ = dic['class'];
          count_object[class_] = count_object[class_] + 1;


         
            count_array[0]++;
          
         
        }
        // updating the chart
        updateBarChart(chart1, count_array);

        // updating the csvData
        var today = new Date();
        csvData += 'Date' + ',' + today + '\n';
        csvData += 'Server' + ',' + camera_id + '\n';
        csvData += 'area' + ',' + lane + '\n';
        csvData += 'Start Time' + ',' + startDate + '\n';
        csvData += 'End Time' + ',' + endDate + '\n';

        csvData += '\n\n';
        csvData += 'Trespassing Counting\n';

        var totalVehicle = 0;
        for (const [key, value] of Object.entries(count_object)) {
          csvData += 'Amount of ' + key + ',' + value + '\n';
          totalVehicle += value;
        }

        csvData += '\n\n';
        csvData += 'Total Trespasser ' + ',' + totalVehicle + '\n';
      },
      error: function (data) {
        alert(data)
      }
    });
  });



  function getServers() {
    $.ajax({
      type: 'GET',
      url: database_url + "/camera/get",
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        temp1.push("</div><option value='All Cameras' >All Cameras</option></div>");
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element._id.$oid + ">" + element.name + "</option></div>");
        });
        $('#inputServer').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }
  getServers();


  $('#generateReport').on('click', function () {
    var fileName = $("#inputFileName").val();

    var dataToEncode;
    dataToEncode = csvData;
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/' + 'csv' + ';charset=utf-8,' + encodeURI(dataToEncode);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'trespassing_counting.' + 'csv';
    hiddenElement.click();
  });

});