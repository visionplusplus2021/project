$(document).ready(function () {

  var dateControl = document.getElementById("startDateTimeInput");
  var todayDate = new Date().toISOString().slice(0, 10)+"T00:00";

  dateControl.value = todayDate ;

  

  var ctx1 = document.getElementById('myChart1').getContext('2d');
  var chart1 = new Chart(ctx1, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
      
      labels: ['','','','',''],
      datasets: [{
        label: ['count'],
        fill: false,
        backgroundColor: [
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
  function updateBarChart(chart, countData,labels,bgColor) {

    chart.data.labels = labels;

    chart.data.datasets.forEach(function (dataset) {
      dataset.data = countData;
      dataset.backgroundColor =bgColor;
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
      url: database_url + "/counting_boundary/get_lane_vehicle/" + data+"_jaywalking",
      success: function (data) {
        var temp1 = [];
        temp1.push("</div><option value=All Areas' >All Areas</option></div>")
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element[0] + ">" + element[2] + "</option></div>");
        });
        $('#inputLane').html(temp1);
      }
    });
  });

  function getData()
  {
    var startDate = document.getElementById("startDateTimeInput").value;
    var endDate = document.getElementById("endDateTimeInput").value; 

    // var startTimestamp = startDate.getTime();
    // var endTimestamp = endDate.getTime();

    var camera_id = $("#inputServer").find('option:selected').val();
    var camera_name = $("#inputServer").find('option:selected').text();
    var area_name = $("#inputLane").find('option:selected').text();
    var area_id = $("#inputLane").find('option:selected').val();
    
    console.log("ssss => "+camera_id);
    if(typeof(camera_id) == "undefined" )
    {
      camera_id = "";
    }

    if(typeof(area_id) == "undefined" )
    {
      area_id = "";
    }


    const data = {
      'start_date': startDate,
      'end_date': endDate,
      'camera_id': camera_id,
      'camera_name': camera_name,
      'area_id': area_id,
      'area_name': area_name
    };
     console.log(data);

    $.ajax({
      type: 'POST',
      url: database_url+'/jaywalking_report/get_by_filter',
      data: data,
      dataType: "text",
      success: function (data) {
        data = JSON.parse(data)

        var count_object = { '': 0, '': 0, 'jaywalker': 0, '': 0, '': 0 }
        var count_array = [];
        var label_array = [];
        var bgColor_array = []
        var arrayLength = data.length;

        var totalJaywalking = 0;
        
        var int_max = 7;
        
        if(arrayLength <6 && arrayLength % 2 !=0){
          int_max = 6;
        }

        for (var i = 0; i < arrayLength; i++) {

          count_array.push(0);
          label_array.push(data[i][0]);
          bgColor_array.push(randomColor());

        }

        

        
        for (var i = 0; i < arrayLength; i++) {
          var dic = data[i];
          class_ = dic['class'];
          count_object[class_] = count_object[class_] + 1;


          
          count_array[i] = data[i][2];
          totalJaywalking = totalJaywalking+ data[i][2];
         
        }


        var count_array_new = [];
        var label_array_new = [];
        var bgColor_array_new = []
        
        for(var i=0; i < Math.trunc((int_max-label_array.length)/2);i++ )
        {
          count_array_new.push(0);
          label_array_new.push("");
          bgColor_array_new.push(randomColor());
        }
        

        for(var i=0; i < count_array.length;i++ )
        {
          count_array_new.push(count_array[i]);
          label_array_new.push(label_array[i]);
          bgColor_array_new.push(randomColor());
        }
        
        for(var i=count_array.length+1; i < int_max-2;i++ )
        {
          count_array_new.push(0);
          label_array_new.push("");
          bgColor_array_new.push(randomColor());
        }


        // updating the chart
        updateBarChart(chart1, count_array_new,label_array_new,bgColor_array_new);

        document.getElementById("lblRecord").innerHTML = "Total "+ totalJaywalking + " Events"

        // updating the csvData
        var today = new Date();
        csvData += 'Date' + ',' + today + '\n';
        csvData += 'Server' + ',' + camera_id + '\n';
        csvData += 'area' + ',' + area_name + '\n';
        csvData += 'Start Time' + ',' + startDate + '\n';
        csvData += 'End Time' + ',' + endDate + '\n';

        csvData += '\n\n';
        csvData += 'Jaywalking Counting\n';

        var totalVehicle = 0;
        for (const [key, value] of Object.entries(count_object)) {
          csvData += 'Amount of ' + key + ',' + value + '\n';
          totalVehicle += value;
        }

        csvData += '\n\n';
        csvData += 'Total Jaywalker ' + ',' + totalVehicle + '\n';
      },
      error: function (data) {
        alert(data)
      }
    });
  }
  $('#applyFilter').on('click', function () {
    getData();
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
          
          if(element[3] == "jaywalking"){
          temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");
          }
        });
        $('#inputServer').html(temp1);
        // $('#inputCameraServer').val("0");

        var temp1 = [];
        temp1.push("</div><option value=All Areas' >All Areas</option></div>")
        $('#inputLane').html(temp1);

      }
    });
  }

  getServers();
  
  getData();

  $('#GenerateReport').on('click', function () {

    console.log('Generating Report');

    var element = document.getElementById('container-fluid-id');
    var opt = {
      margin:       0,
      filename:     'jaywalking.pdf',
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
    hiddenElement.download = 'jaywalking_counting.' + 'csv';
    hiddenElement.click();
  });

});