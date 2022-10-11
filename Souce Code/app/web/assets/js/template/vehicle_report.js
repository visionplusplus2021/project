$(document).ready(function () {

  var dateControl = document.getElementById("startDateTimeInput");
  var todayDate = new Date().toISOString().slice(0, 10)+"T00:00";

  dateControl.value = todayDate ;

  var ctx1 = document.getElementById('myChart1').getContext('2d');

  var chart_data = `{
    label: ['count'],
    fill: false,
    backgroundColor: [
      randomColor(),
      randomColor(),
      randomColor(),
      randomColor(),
      randomColor()
    ],
    // borderColor: 'rgb(255, 99, 132)',
    data: []
  },
  {
    label: ['count'],
    fill: false,
    backgroundColor: [
      randomColor(),
      randomColor(),
      randomColor(),
      randomColor(),
      randomColor()
    ],
    // borderColor: 'rgb(255, 99, 132)',
    data: []
  }`;

  var chart1 = new Chart(ctx1, {
    // The type of chart we want to create

    
    type: 'bar',

      
    // The data for our dataset
    data: {
      labels: ['bicycle', 'car', 'motorbike', 'bus', 'truck'],
      datasets: [
        {

          label: ['count'],
          fill: false,
          backgroundColor: [
            randomColor(),
            randomColor(),
            randomColor(),
            randomColor(),
            randomColor()
          ],
          // borderColor: 'rgb(255, 99, 132)',
          data: []
        }
    ]
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
      url: database_url + "/counting_boundary/get_lane_vehicle/" + data+"_vehicle",
      success: function (data) {
        var temp1 = [];
        temp1.push("</div><option value=All Lanes' >All Lanes</option></div>")
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element[0] + ">" + element[2] + "</option></div>");
        });
        $('#inputLane').html(temp1);
      }
    });
  });

  $('#applyFilter').on('click', function () {
    getData();
  });

  getData();

  function getData()
  {
    var startDate = document.getElementById("startDateTimeInput").value;
    var endDate = document.getElementById("endDateTimeInput").value; 

    // var startTimestamp = startDate.getTime();
    // var endTimestamp = endDate.getTime();

    var camera_id = $("#inputServer").find('option:selected').val();
    var lane = $("#inputLane").find('option:selected').text();

    if(typeof(camera_id) == "undefined" )
    {
      camera_id = "";
    }

    if(typeof(lane) == "undefined" )
    {
      lane = "";
    }

    const data = {
      'start_date': startDate,
      'end_date': endDate,
      'camera_id': camera_id,
      'lane_name': lane
    };
    // console.log(data);
  
    
    $.ajax({
      type: 'POST',
      url: database_url+'/vehicle/get_by_filter',
      data: data,
      dataType: "text",
      success: function (data) {
        data = JSON.parse(data)
        
        
        var count_object = { 'bicycle': 0, 'car': 0, 'motorbike': 0, 'bus': 0, 'truck': 0 }
        var count_array = [0, 0, 0, 0, 0, 0];

        var arrayLength = data.length;

        var totalJaywalking = 0;
        for (var i = 0; i < arrayLength; i++) {


          var dic = data[i];
          class_ = data[i][0];
          count_object[class_] = count_object[class_] + 1;

          totalJaywalking = totalJaywalking+data[i][1];
          if (class_ == 'bicycle') {
            count_array[0] = data[i][1]
          }
          else if (class_ == 'car') {
            count_array[1] = data[i][1]
          }
          else if (class_ == 'motorbike') {
            count_array[2] = data[i][1]
          }
          else if (class_ == 'bus') {
            count_array[3] = data[i][1]
          }
          else {
            count_array[4] = data[i][1];
          }
        }
        // updating the chart
        updateBarChart(chart1, count_array);

        document.getElementById("lblRecord").innerHTML = "Total "+ totalJaywalking + " Vehicles"
        // // updating the csvData
        // var today = new Date();
        // csvData += 'Date' + ',' + today + '\n';
        // csvData += 'Server' + ',' + camera_name + '\n';
        // csvData += 'Lane' + ',' + lane + '\n';
        // csvData += 'Start Time' + ',' + startDate + '\n';
        // csvData += 'End Time' + ',' + endDate + '\n';

        // csvData += '\n\n';
        // csvData += 'Vehicle Counting\n';

        // var totalVehicle = 0;
        // for (const [key, value] of Object.entries(count_object)) {
        //   csvData += 'Amount of ' + key + ',' + value + '\n';
        //   totalVehicle += value;
        // }

        // csvData += '\n\n';
        // csvData += 'Total Vahicle ' + ',' + totalVehicle + '\n';
      },
      error: function (data) {
        alert(data)
      }
    });
  }

  function getServers() {
    $.ajax({
      type: 'GET',
      url: database_url + "/camera/get",
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        temp1.push("</div><option value='All Cameras' >All Cameras</option></div>");
        JSON.parse(data).forEach(function (element, index) {
          
          if(element[3] == "counting"){
            temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");
            }
        });
        $('#inputServer').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }
  getServers();

  $('#GenerateReport').on('click', function () {

    console.log('Generating Report');

    var element = document.getElementById('container-fluid-id');
    var opt = {
      margin:       0,
      filename:     'vehicle.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2 },
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
    };

    // New Promise-based usage:
    html2pdf().set(opt).from(element).save();

    // Old monolithic-style usage:
    // html2pdf(element, opt);

  });
  $('#generateReport').on('click', function () {
    var fileName = $("#inputFileName").val();

    var dataToEncode;
    dataToEncode = csvData;
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/' + 'csv' + ';charset=utf-8,' + encodeURI(dataToEncode);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'vehicle_counting.' + 'csv';
    hiddenElement.click();
  });

});