$(document).ready(function () {
  

  var dateControl = document.getElementById("startDateTimeInput");
  var todayDate = new Date().toISOString().slice(0, 10)+"T00:00";

  dateControl.value = todayDate ;
  getData();


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

    video_source = "./event/jaywalking/" + fileName  ;
    console.log("my video source: "+video_source);

    $('source').attr("src", video_source);
    $('video')[0].load();
    $('video')[0].play();
  });

  $('#ModalDeleteServer').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteServer').click(function () {
    
    var fileName = $('#ModalDeleteServer').data('oid');
    

    $.ajax({
      type: 'DELETE',
      url: database_url + "/event/delete/" + fileName,
      success: function (data) {
        location.reload();
      }
    });
  });

  function getServers() {
    $.ajax({
      type: 'GET',
      url: database_url + "/camera/get_jaywalking_camera",
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
    getData();
  });

  function getData()
  {
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
        
        var int_row = 0
        $('#events').html("");
        JSON.parse(data).forEach(function (element, index) {  
          
          int_row+=1
          server = element[8] +":"+element[9]
          $("#events").append(
            '<tr>' + 
                  '<td>' + element[3]+ '</td>' +
                  '<td>' + element[4] + '</td>' +
                  '<td>' + element[7] + '</td>' +
                  '<td>' + element[5] + '</td>' +
                  '<td><button class="btn btn-info btn-sm" data-toggle="modal" data-target="#viewEvent" data-fileName='+ element[2] + ' data-event_type='+ element[5] + ' data-server='+ server + ' id="buttonViewEvent" >View</button></td>' +
                  "<td><button class='btn btn-danger btn-sm' data-title='Delete' data-fileName='"+ element[2]+"'  data-id='" + element[2]  + "' data-toggle='modal' data-target='#ModalDeleteServer' id='buttonModalDeleteServer'>Delete</button></td>" +
                '</tr>'
          );
        });

        document.getElementById("lblRecord").innerHTML = "Showing "+ int_row + " entries"
      },
      error: function (data) {
        alert(data)
      }
    });
  }
  
  
  
});