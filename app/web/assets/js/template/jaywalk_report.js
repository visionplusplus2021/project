$(document).ready(function () {


    $('#inputServer').change(function(){
      // var data= $(this).val();
      var data= $(this).find('option:selected').text();

      $.ajax({
        type: 'GET',
        url: database_url + "/lane/get/"+data,
        success: function (data) {
          // var temp1 = ["<option value='0'>Unlisted</div>"];
          var temp1 = [];
          JSON.parse(data).forEach(function (element, index) {
            temp1.push("</div><option value=" + element._id.$oid + ">" + element.from + " to " + element.to + "</option></div>");
          });
          $('#inputLane').html(temp1);
          // $('#inputCameraServer').val("0");
        }
      });

      // alert(data);
    });

    $('#applyFilter').on('click', function () {
        var startDate = new Date($("#startDateTimeInput").val());
        var endDate = new Date($("#endDateTimeInput").val());

        // var startTimestamp = parseFloat(startDate.getTime())/1000.0;
        // var endTimestamp = parseFloat(endDate.getTime())/1000.0;

        var startTimestamp = startDate.getTime();
        var endTimestamp = endDate.getTime();

        var server = $("#inputServer").find('option:selected').text();
        var lane = $("#inputLane").find('option:selected').text();
        var fileName = $("#inputFileName").val();

        lane_tokenized = lane.split(" ");
        lane_from = lane_tokenized[0];
        lane_to = lane_tokenized[2];


        // console.log('Start Date: ' + startDate);
        // console.log('End Date: ' + endDate);
        console.log('Start Date: ' + startTimestamp);
        console.log('End Date: ' + endTimestamp);
        console.log('Server: ' + server);
        console.log('From: ' + lane_from);
        console.log('To: ' + lane_to);
        console.log('fileName: ' + fileName);


        // generateReport(fileName, from, to, startTimestamp, endTimestamp);

      const data = {
        'start': startTimestamp,
        'end': endTimestamp,
        'server': server,
        'from': lane_from,
        'to': lane_to
      };
      // console.log(data);

      var database_url = database_url + '/vehicle/get_by_filter';
      $.ajax({
        type: 'POST',
        url: database_url,
        data: data,
        dataType: "text",
        success: function (data) {
          data = JSON.parse(data)

          count = {'bicycle': 0, 'car': 0, 'motorbike': 0, 'bus': 0, 'truck': 0}

          var arrayLength = data.length;
          for (var i = 0; i < arrayLength; i++) {
              var dic = data[i];
              class_ = dic['class'];
              count[class_] = count[class_] + 1;
          }

          var today = new Date();
          var csvData = 'Date' + ',' + today + '\n';
          csvData += 'Server' + ',' + server + '\n';
          csvData += 'Lane' + ',' + lane + '\n';
          csvData += 'Start Time' + ',' + startDate + '\n';
          csvData += 'End Time' + ',' + endDate + '\n';

          csvData += '\n\n';
          csvData += 'Vehicle Counting\n';

          var totalVehicle = 0;
          for (const [key, value] of Object.entries(count)) {
            csvData += 'Amount of ' + key + ',' + value + '\n';
            totalVehicle += value;
          }

          csvData += '\n\n';
          csvData += 'Total Vahicle ' + ',' + totalVehicle + '\n';

          var dataToEncode;
          dataToEncode = csvData;
          var hiddenElement = document.createElement('a');
          hiddenElement.href = 'data:text/' + 'csv' + ';charset=utf-8,' + encodeURI(dataToEncode);
          hiddenElement.target = '_blank';
          hiddenElement.download = fileName + '.' + 'csv';
          hiddenElement.click();
          // **********************************************************
        },
        error: function (data) {
          alert("Please check all fields.")
        }
      });


    });

    function getServers() {
      $.ajax({
        type: 'GET',
        url: database_url + "/server/get",
        success: function (data) {
          // var temp1 = ["<option value='0'>Unlisted</div>"];
          var temp1 = [];
          JSON.parse(data).forEach(function (element, index) {
            temp1.push("</div><option value=" + element._id.$oid + ">" + element.server_ip + ":" + element.server_port + "</option></div>");
          });
          $('#inputServer').html(temp1);
          // $('#inputCameraServer').val("0");
        }
      });
    }
    getServers();

    async function generateReport(fileName, from_, to_, startTimestamp_, endTimestamp_) {
      // console.log('sample message');

      const data = {
        'from': from_,
        'to': to_,
        'startTimestamp': startTimestamp_,
        'endTimestamp': endTimestamp_
      };
      console.log(data);

      var database_url = database_url + '/report/get';
      fetch(database_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => {

        // console.log('Success:', data);
        var csvData = 'timestamp' + ',' + 'from' + ',' + 'to' + ',' + 'class' + ',' + 'id';
        csvData += '\n';

        var arrayLength = data.length;
        for (var i = 0; i < arrayLength; i++) {
            // console.log(data[i]);
            var dic = data[i];

            // intTimestamp = parseInt();
            // stringTimestamp = intTimestamp.toString();
            // trimmedTimestamp = stringTimestamp.substring(0,10);
            // console.log(trimmedTimestamp);

            var date = new Date(dic['timestamp']);
            var formatted_datetime = date.getFullYear() + "-" + ("0" + (date.getMonth() + 1)).slice(-2) + "-" + ("0" + date.getDate()).slice(-2) + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2) + ":" + ("0" + date.getSeconds()).slice(-2);

            csvData += formatted_datetime + ',' + dic['from'] + ',' + dic['to'] + ',' + dic['class'] + ',' + dic['id'];
            csvData += '\n';
        }

        var dataToEncode;
        dataToEncode = csvData;
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/' + 'csv' + ';charset=utf-8,' + encodeURI(dataToEncode);
        hiddenElement.target = '_blank';
        hiddenElement.download = fileName + '.' + 'csv';
        hiddenElement.click();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }


    $('#cancelTimeFilter').on('click', function () {
    });

  });