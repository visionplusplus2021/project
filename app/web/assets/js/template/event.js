$(document).ready(function () {

  // $.ajax({
  //   type: 'GET',
  //   url: database_url + "/event/get_by_filter",
  //   success: function (data) {
  //     JSON.parse(data).forEach((element, index) => {
  //       // console.log(element);
  //       $("#events").append(
  //         '<tr>' + 
  //               '<td>' + element.timestamp + '</td>' +
  //               '<td>' + element.server + '</td>' +
  //               '<td>' + element.camera_name + '</td>' +
  //               '<td>' + element.event_type + '</td>' +
  //               '<td><button class="btn-info btn" data-toggle="modal" data-target="#viewEvent" data-id='+ element.file_name + ' id="buttonViewEvent" >View</button></td>' +
  //             '</tr>'
  //       );
  //     });
  //   }
  // });

  

  $('#viewEvent').on('shown.bs.modal', function (e) {
    var event_type = $(e.relatedTarget).attr('data-event_type');
    var fileName = $(e.relatedTarget).attr('data-fileName');
    var server = $(e.relatedTarget).attr('data-server');
    // console.log(event_type);
    // console.log(fileName);

    // $('img').attr("src", "http://127.0.0.1:7001/event_view/" + event_type + "/" + fileName);

    video_source = "./event/jaywalking/1.avi"  ;
    console.log("my video source: "+video_source);

    $('source').attr("src", video_source);
    $('video')[0].load();
    $('video')[0].play();
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
          temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");
        });
        $('#inputServer').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }
  getServers();


  $('#applyFilter').on('click', function () {
    var startDate = document.getElementById("startDateTimeInput").value;
    var endDate = document.getElementById("endDateTimeInput").value; 

    // var startTimestamp = startDate.getTime();
    // var endTimestamp = endDate.getTime();
    
    var server = $("#inputServer").find('option:selected').text();
    var event_type = $("#inputEventType").find('option:selected').text();

    const data = {
      'start_date': startDate,
      'end_date': endDate,
      'server': server,
      'event_type': event_type
    };
    
    $.ajax({
      type: 'POST',
      url: database_url+'/event/get_by_filter',
      data: data,
      dataType: "text",
      success: function (data) {
        // console.log(data);

        $('#events').html("");
        JSON.parse(data).forEach(function (element, index) {  
          console.log("===> "+element[7]);
          
          server = element[8] +":"+element[9]
          $("#events").append(
            '<tr>' + 
                  '<td>' + element[3]+ '</td>' +
                  '<td>' + element[4] + '</td>' +
                  '<td>' + element[7] + '</td>' +
                  '<td>' + element[5] + '</td>' +
                  '<td><button class="btn-info btn" data-toggle="modal" data-target="#viewEvent" data-fileName='+ element[2] + ' data-event_type='+ element[5] + ' data-server='+ server + ' id="buttonViewEvent" >View</button></td>' +
                '</tr>'
          );
        });
      },
      error: function (data) {
        alert(data)
      }
    });
  });


  
  
  
});