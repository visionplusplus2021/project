$(document).ready(function () {

  $('#buttonCameraAdd').click(function () {

    var updateOID = $('#ModalUpdateCamera').data('oid');
    var cameraName = $("#inputCameraName").val();
    var cameraURL = $("#inputCameraURL").val();
    var cameraAreaID = $("#inputCameraArea").val();
    var $status = $("#statusAdd");



    if (cameraName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Camera Stream Name').removeClass("invisible");
    }
    else if (cameraURL == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Camera Stream URL').removeClass("invisible");
    }
    else if (isNaN(lat) || isNaN(lng)) {
      $status.css({ "color": "red" });
      $status.text('Please Select Camera Stream Location').removeClass("invisible");
    }

    else {




      // $.ajax({
      //   type: 'GET',
      //   url: database_url + "/camera_stream/get",
      //   success: function (data) {
      //     JSON.parse(data).forEach(element => {
      //       if (element.name == cameraName && element.url == cameraURL) {
      //         console.log(element.server);
      //         $('#updateCameraName').val(element.name);
      //         $('#updateCameraURL').val(element.url);
      //         updateOID = element._id.$oid
      //       }
      //     })
      //   }
      // });


      console.log("Obj ID " + updateOID)
      const data = {
        'object_id': updateOID,
        'name': cameraName,
        'url': cameraURL,
        'latitude': lat,
        'longitude': lng,
        'area_id': cameraAreaID,
        'user_id': user_id
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/camera_stream/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          
          if (data.status == 422) {
            
            $status.css({ "color": "red" });
            $status.text('Camera Stream Name already exists').removeClass("invisible");
          }
          else {
            location.reload()
          }
        }
      });

    }

  });




  $('#buttonCameraUpdate').click(function () {
    var updateOID = $('#ModalUpdateCamera').data('oid');
    var cameraName = $("#updateCameraName").val();
    var cameraURL = $("#updateCameraURL").val();
    var cameraAreaID = $("#updateCameraArea").val();

    var $status = $("#statusUpdate");



    if (cameraName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Camera Stream Name').removeClass("invisible");
    }
    else if (cameraURL == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Camera Stream URL').removeClass("invisible");
    }
    else if (isNaN(lat) || isNaN(lng)) {
      $status.css({ "color": "red" });
      $status.text('Please Select Camera Stream Location').removeClass("invisible");
    }

    else {


      var database_endpoint = database_url + '/camera_stream/update';
      data = {
        'object_id': updateOID,
        'area_id': cameraAreaID,
        'name': cameraName,
        'url': cameraURL,
        'latitude': lat,
        'longitude': lng,
        'user_id': user_id
      };

      console.log("This is the update value: ");
      console.log(data);


      $.ajax({
        type: 'PUT',
        url: database_url + "/camera_stream/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
         
          if (data.status == 422) {
            $status.css({ "color": "red" });
            $status.text('Camera Stream Name already exists').removeClass("invisible");
          }
          else {
            location.reload()
          }

        }
      });
    }
  });


  $('#ModalDeleteCamera').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

  });

  $('#buttonDeleteCamera').click(function () {
    var camID = $('#ModalDeleteCamera').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/camera_stream/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#buttonCamStreamActivate').click(function () {
    var updateOID = $('#ModalActivateCamStream').data('oid');

    console.log("my id: " + updateOID);

    $.ajax({
      type: 'POST',
      url: database_url + "/camera_stream/activate/" + updateOID + "_" + user_id,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateCamStream').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });



  $('#ModalUpdateCamera').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id');
    $(this).data("oid", objectID);

    $.ajax({
      type: 'GET',
      url: database_url + "/camera_stream/getByID/" + objectID,
      success: function (data) {


        JSON.parse(data).forEach(element => {

          // console.log("my ID " + element);
          $('#updateCameraID').val(objectID);
          $('#updateCameraName').val(element[2]);
          $('#updateCameraURL').val(element[4]);
          $('#updateCameraArea').val(element[1]);

        })
      }
    });


  });

  $.ajax({
    type: 'GET',
    url: database_url + "/camera_stream/get",
    success: function (data) {

      JSON.parse(data).forEach((results, index) => {

        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateCamStream' id='buttonModalActivateCamStream' title='Click for Activation'>Activate</a></td>"
        if (results[7] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateCamStream' id='buttonModalActivateCamStream' title='Click for Inactivation' >Inactivate</a></td>"
        }

        $("#showContact").append("<tr><td>" + results[2] + "</td><td>" +
          results[3] + "</td><td>" +
          results[4] + "</td><td>" +
          results[5] + "</td><td>" +
          results[6] + "</td><td>" +

          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateCamera' id='buttonModalUpdateCamera'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteCamera' id='buttonModalDeleteCamera'>Delete</a></td><td>" +
          str_activate +
          "</tr>")
      })
    }
  })

  getCameraAreas();
});

function getCameraAreas() {
  $.ajax({
    type: 'GET',
    url: database_url + "/camera_area/getActive",
    success: function (data) {
      // var temp1 = ["<option value='0'>Unlisted</div>"];
      var temp1 = [];
      JSON.parse(data).forEach(function (element, index) {
        console.log("caemra stream: " + element[0]);
        temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");
      });
      $('#inputCameraArea').html(temp1);
      $('#updateCameraArea').html(temp1);
      // $('#inputCameraServer').val("0");
    }
  });
}












































// these are the codes for working in server


// $(document).ready(function () {

//     $('#buttonServerAdd').click(function () {

//       var $status = $("#statusAdd");

//       var serverName = $("#inputServerName").val();
//       var serverIP = $("#inputServerIP").val();
//       var serverPort = $("#inputServerPort").val();
//       var serverType = $("#inputServerType").val();

//       console.log('Server Name: ' + serverName);
//       console.log('Server IP: ' + serverIP);
//       console.log('Server Port: ' + serverPort);
//       console.log('Server Type: ' + serverType);

//       if (serverName == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server Name.').removeClass("invisible");
//       }
//       else if (serverIP == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server IP.').removeClass("invisible");
//       }
//       else if (serverPort == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server Port').removeClass("invisible");
//       }
//       else {
//         // save group information in database
//         const data = {
//           'serverName': serverName.toLowerCase().trim(),
//           'serverIP': serverIP,
//           'serverPort': serverPort,
//           'serverType': serverType,
//           'serverActivate': 'true',
//           'serverUsed': 'false'
//         };

//         $.ajax({
//           type: 'POST',
//           url: "http://127.0.0.1:8003/server/store",
//           data: data,
//           dataType: "text",
//           success: function (data) {
//             location.reload()
//           },
//           error: function (data) {
//             if( data.status == 44 ){
//               $status.css({ "color": "red" });
//               $status.text(" 'Server Name' already exists").removeClass("invisible");
//             }
//             else{
//             location.reload()
//             }

//           }

//         });
//       }
//     });

//     $('#buttonServerUpdate').click(function () {
//       var $status = $("#statusUpdate");

//       var updateOID = $('#ModalUpdateServer').data('oid');
//       var serverName = $("#updateServerName").val();
//       var serverIP = $("#updateServerIP").val();
//       var serverPort = $("#updateServerPort").val();
//       var serverType = $("#updateServerType").val();


//       if (serverName == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server Name.').removeClass("invisible");
//       }
//       else if (serverIP == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server IP.').removeClass("invisible");
//       }
//       else if (serverPort == '') {
//         $status.css({ "color": "red" });
//         $status.text('Please Enter Server Port').removeClass("invisible");
//       }
//       else {
//         // save group information in database
//         const data = {
//           'object_id': updateOID,
//           'serverName': serverName.toLowerCase().trim(),
//           'serverIP': serverIP,
//           'serverPort': serverPort,
//           'serverType': serverType
//         };

//         $.ajax({
//           type: 'PUT',
//           url: "http://127.0.0.1:8003/server/update",
//           data: data,
//           dataType: "text",
//           success: function (data) {
//             location.reload();
//           },
//           error: function (data) {
//             console.log(data.status)
//             if( data.status == 44 ){
//               $status.css({ "color": "red" });
//               $status.text(" 'Server Name' already exists").removeClass("invisible");
//             }


//           }
//         });
//       }
//     });

//     $('#ModalUpdateServer').on('show.bs.modal', function (e) {
//       var objectID = $(e.relatedTarget).attr('data-id')
//       $(this).data("oid", $(e.relatedTarget).attr('data-id'));

//       $.ajax({
//         type: 'GET',
//         url: "http://127.0.0.1:8003/server/get",
//         success: function (data) {
//           JSON.parse(data).forEach(element => {
//             if (element._id.$oid == objectID) {
//               console.log(element.server);
//               $('#updateServerName').val(element.server_name);
//               $('#updateServerIP').val(element.server_ip);
//               $('#updateServerPort').val(element.server_port);
//               $("#updateServerType option:selected").text(element.server_type);
//               $('#updateServerActivate').val(element.server_activate);
//             }
//           })
//         }
//       });
//     });

//     $('#ModalActivateServer').on('show.bs.modal', function (e) {
//       $(this).data("oid", $(e.relatedTarget).attr('data-id'));
//     });

//     $('#buttonServerActivate').click(function () {
//       var updateOID = $('#ModalActivateServer').data('oid');


//       $.ajax({
//         type: 'POST',
//         url: "http://127.0.0.1:8003/server/activate/" + updateOID,
//         success: function (data) {
//           location.reload();
//         }
//       });
//     });



//     $('#ModalDeleteServer').on('show.bs.modal', function (e) {
//       $(this).data("oid", $(e.relatedTarget).attr('data-id'));
//     });

//     $('#buttonDeleteServer').click(function () {
//       var camID = $('#ModalDeleteServer').data('oid');

//       $.ajax({
//         type: 'DELETE',
//         url: "http://127.0.0.1:8003/server/delete/" + camID,
//         success: function (data) {
//           location.reload();
//         }
//       });
//     });


//     $.ajax({
//       type: 'GET',
//       url: "http://127.0.0.1:8003/server/get",
//       success: function (data) {


//         JSON.parse(data).forEach((results, index) => {
//           myFunction(results.server_ip + ":" + results.server_port);
//           var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateServer' id='buttonModalActivateServer' title='Click for Activate' >Inactivated</a></td>"
//           if (results.server_activate == "true") {
//             str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateServer' id='buttonModalActivateServer' title='Click for Inactivate'>Activated</a></td>"
//           }

//           str_server_used = "available </td><td>"
//           if (results.server_used == "true") {
//             str_server_used = "used </td><td>"
//           }

//           $("#showContact").append("<tr><td>" + results.server_name + "</td><td>" +
//             results.server_ip + "</td><td>" +
//             results.server_port + "</td><td>" +
//             results.server_type + "</td><td>" +

//             str_server_used +

//             "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalUpdateServer' id='buttonModalUpdateServer'>Edit</a></td><td>" +
//             "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteServer' id='buttonModalDeleteServer'>Delete</a></td><td>" +
//             str_activate +
//             "</tr>")
//         })
//       }
//     })
//   });




//   function myFunction(ip) {


//   }
