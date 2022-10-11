//Select Contact




$(document).ready(function () {

  $('#buttonServerAdd').click(function () {

    var $status = $("#statusAdd");

    var serverName = $("#inputServerName").val();
    var serverIP = $("#inputServerIP").val();
    var serverPort = $("#inputServerPort").val();
    var serverType = $("#inputServerType").val();

    console.log('Server Name: ' + serverName);
    console.log('Server IP: ' + serverIP);
    console.log('Server Port: ' + serverPort);
    console.log('Server Type: ' + serverType);

    if (serverName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Name.').removeClass("invisible");
    }
    else if (serverIP == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server IP.').removeClass("invisible");
    }
    else if (serverPort == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Port').removeClass("invisible");
    }
    else {

      // create an XHR object
      var request = new XMLHttpRequest();
      var params = "UID=CORS&name=CORS";
      request.timeout = 5000;

      request.onreadystatechange = function () {


        console.log("request.readyState:"+request.readyState+ ", request.status"+request.status)
        //Connect to the server sucessfully
        if (request.readyState === 4) {
          if (request.status === 200) {

            // //check the server  
            $.ajax({
              type: 'GET',
              dataType: 'json',
              url: "http://199.212.33.166:6101/run_server_port/"+serverPort,
              // url: "http://" + serverIP + ":" + serverPort + "/test_camera_connection/"+serverPort,

              success: function (res) {

                
                // save group information in database
                const data_insert = {
                  'serverName': serverName.toLowerCase().trim(),
                  'serverIP': serverIP,
                  'serverPort': serverPort,
                  'serverType': serverType,
                  'serverActivate': 'true',
                  'serverUsed': 'false',
                  'user_id':user_id
                };

                $.ajax({
                  type: 'POST',
                  url: database_url + "/server/store",
                  data: data_insert,
                  dataType: "text",
                  success: function (data) {
                    location.reload();
                  },
                  error: function (data) {
                    if (data.status == 422) {
                      $status.css({ "color": "red" });
                      $status.text(" 'Server' already exists").removeClass("invisible");
                    }
                    else {
                      console.log("error")
                    }

                  }

                });

              },
              error: function (res) {
                
                $status.css({ "color": "red" });
                $status.text("Cannot connect to the 'server:" + serverIP + ":" + serverPort + "'").removeClass("invisible");
              }

            });

            
          }
        }
      };
     
      request.open('GET', "http://199.212.33.166:6999/test_camera_connection/"+serverPort, true);
      request.send(params);


      // //check the server  
      // $.ajax({
      //   type: 'GET',
      //   dataType: 'json',
      //   url: "http://199.212.33.166:9905/test_camera_connection/"+serverPort,
      //   // url: "http://" + serverIP + ":" + serverPort + "/test_camera_connection/"+serverPort,

      //   success: function (res) {

          
      //     // save group information in database
      //     const data_insert = {
      //       'serverName': serverName.toLowerCase().trim(),
      //       'serverIP': serverIP,
      //       'serverPort': serverPort,
      //       'serverType': serverType,
      //       'serverActivate': 'true',
      //       'serverUsed': 'false',
      //       'user_id':user_id
      //     };

      //     $.ajax({
      //       type: 'POST',
      //       url: database_url + "/server/store",
      //       data: data_insert,
      //       dataType: "text",
      //       success: function (data) {
      //         location.reload();
      //       },
      //       error: function (data) {
      //         if (data.status == 422) {
      //           $status.css({ "color": "red" });
      //           $status.text(" 'Server Name' already exists").removeClass("invisible");
      //         }
      //         else {
      //           console.log("error")
      //         }

      //       }

      //     });

      //   },
      //   error: function (res) {
          
      //     $status.css({ "color": "red" });
      //     $status.text("Cannot connect to the 'server:" + serverIP + ":" + serverPort + "'").removeClass("invisible");
      //   }

      // });

    }
  });

  $('#buttonServerUpdate').click(function () {
    var $status = $("#statusUpdate");

    var updateOID = $('#ModalUpdateServer').data('oid');
    var serverName = $("#updateServerName").val();
    var serverIP = $("#updateServerIP").val();
    var serverPort = $("#updateServerPort").val();
    var serverType = $("#updateServerType").val();


    if (serverName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Name.').removeClass("invisible");
    }
    else if (serverIP == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server IP.').removeClass("invisible");
    }
    else if (serverPort == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Port').removeClass("invisible");
    }
    else {
      //check the server 
      $.ajax({
        type: 'GET',
        dataType: 'json',
        url: "http://" + serverIP + ":" + serverPort + "/test_camera_connection/1",

        success: function (res) {
          // save group information in database
          const data = {
            'object_id': updateOID,
            'serverName': serverName.toLowerCase().trim(),
            'serverIP': serverIP,
            'serverPort': serverPort,
            'serverType': serverType,
            'user_id':user_id
          };

          $.ajax({
            type: 'PUT',
            url: database_url + "/server/update",
            data: data,
            dataType: "text",
            success: function (data) {
              location.reload();
            },
            error: function (data) {
              console.log(data.status)
              if (data.status == 422) {
                $status.css({ "color": "red" });
                $status.text(" 'Server Name' already exists").removeClass("invisible");
              }


            }
          });

        },
        error: function (res) {
          $status.css({ "color": "red" });
          $status.text("Cannot connect to the 'server:" + serverIP + ":" + serverPort + "'").removeClass("invisible");
        }
      });
    }
  });

  $('#ModalUpdateServer').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/server/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          
            
            $('#updateServerName').val(element[3]);
            $('#updateServerIP').val(element[4]);
            $('#updateServerPort').val(element[5]);
            $("#updateServerType option:selected").text(element[2]);
            $('#updateServerActivate').val(element[6]);
          
        })
      }
    });
  });

  
  $('#ModalAddServer').on('show.bs.modal', function (e) {
    getServerInfo();
  });


  $('#ModalActivateServer').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonServerActivate').click(function () {
    var updateOID = $('#ModalActivateServer').data('oid');


    $.ajax({
      type: 'POST',
      url: database_url + "/server/activate/" + updateOID,
      success: function (data) {
        location.reload();
      }
    });
  });



  $('#ModalDeleteServer').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteServer').click(function () {
    var camID = $('#ModalDeleteServer').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/server/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $.ajax({
    type: 'GET',
    url: database_url + "/server/get",
    success: function (data) {


      JSON.parse(data).forEach((results, index) => {
        
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateServer' id='buttonModalActivateServer' title='Click for Activation' >Activate</a></td>"
        if (results[6] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateServer' id='buttonModalActivateServer' title='Click for Inactivation'>Inactivate</a></td>"
        }

        str_server_used = "available </td><td>"
        if (results[7] == true) {
          str_server_used = "used </td><td>"
        }

        $("#showContact").append("<tr><td>" + results[3] + "</td><td>" +
          results[2] + "</td><td>" +
          results[4] + "</td><td>" +
          results[5] + "</td><td>" +

          str_server_used +

          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalUpdateServer' id='buttonModalUpdateServer'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalDeleteServer' id='buttonModalDeleteServer'>Delete</a></td><td>" +
          str_activate +
          "</tr>")
      })
    }
  })

  getServerType();
  
});

$('#inputServerIP').change(function () {
  
  getServerInfo()
 
});


function getServerInfo() {

  let element = document.getElementById("serverinfo");
  let inputServerIP = $("#inputServerIP").val();
  element.innerHTML ="";
  
  $.ajax({
    type: 'GET',
    url: "http://"+inputServerIP+":6101/get_server_info",
    success: function (data) {
      str_data = data.split("[");

      
      element.innerHTML = "<h6>Server Information </h6>&emsp;["+str_data[1]+"<br/>&emsp;["+str_data[2];

      
      // $serverinfo.text("["+str_data[1]+  ).removeClass("invisible");
      
      
    }
  });
}


function getServerType() {
  $.ajax({
    type: 'GET',
    url: database_url + "/server_type/get_activate",
    success: function (data) {
      // var temp1 = ["<option value='0'>Unlisted</div>"];
      var temp1 = [];
      JSON.parse(data).forEach(function (element, index) {
       
        temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");
      });
      $('#inputServerType').html(temp1);
      $('#updateServerType').html(temp1);
      // $('#inputCameraServer').val("0");
    }
  });
}
