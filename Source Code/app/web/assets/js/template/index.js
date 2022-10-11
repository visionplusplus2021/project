$(document).ready(function () {

  var gl_camera_id = ""
  var gl_boundary_event
  var gl_server = ""
  let xhr = new XMLHttpRequest();
  updateOID = ""

  renderCards();
  getServers("1");
  getCameraStreams();



  $('#buttonCameraAdd').click(function () {
    $("#ModalAddCamera").modal('hide')
    var updateOID = ""
    var cameraName = $("#inputCameraName").val();
    var cameraStream = $("#inputCameraURL option:selected").val();
    var cameraURLName = $("#inputCameraURL option:selected").text();
    var cameraServer = $("#inputCameraServer option:selected").text();
    var cameraServerID = $("#inputCameraServer option:selected").val();
    var cameraGroup = $("#inputCameraGroup option:selected").val();
    _cameraID = ""



    gl_server = cameraServer
    $.ajax({
      type: 'GET',
      url: database_url + "/camera/getByName/" + cameraName,
      success: function (data) {

        JSON.parse(data).forEach(element => {

          $('#updateCameraName').val(element[1]);
          $('#updateCameraURL option:selected').text(element[6]);

          $('#updateCameraGroup').val(element[2]);
          $("#updateCameraServer option:selected").text(element[8]);


          updateOID = element[0]


        })
      }
    });

    
    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get_isActivate",
      success: function (list) {
        var temp = [];
        var features = [];
        alert("Add New Camera");
        JSON.parse(list).forEach(element => {
          if ($('input#inputFeature' + element[0]).prop('checked') == true) {

            features.push(element[0]);
          }



        })

        


        var database_endpoint = database_url + '/camera/update';
        const data = {
          'object_id': updateOID,
          'camera_name': cameraName,
          'camera_stream': cameraStream,
          'camera_url_name': cameraURLName,
          'camera_group': cameraGroup,
          'camera_serverID': cameraServerID,
          'features': features,
          'user_id': user_id
        };

        fetch(database_endpoint, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then(response => {
            if (response.status == 422) {
              alert("Camera ID already exists")
            }
            location.reload();
          })
          .then(data => {



            $("#saveInfo").css("display", "none");
            $("#buttonCameraAdd").attr("disabled", false);
            $('#Features').removeClass('disabled');

            renderCards();

          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    });



  });


  $('#ModalConfirmAddLane').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });
  $('#buttonConfirmAddLane').click(function () {

  }
  );


  $('#ModalDeleteLane').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalDeleteCamera').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

  });

  $('#buttonDeleteCamera').click(function () {
    //var camID = $('#ModalDeleteCamera').data('oid');

    var keys = $('#ModalDeleteCamera').data('oid');

    str_keys = keys.split("_");
    camID = str_keys[0]
    serverIP = str_keys[1]


    $.ajax({
      type: 'DELETE',
      url: database_url + "/camera/delete/" + camID,
      success: function (data) {
        location.reload();
      }

    });

  });

  $('#ModalAddCamera').on('show.bs.modal', function (e) {
    


    getUpdateFeatures("1","1","1");
    
    getServers("1");



  });

  $('#ModalUpdateCamera').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id');

    $(this).data("oid", objectID);



    $.ajax({
      type: 'GET',
      url: database_url + "/camera/getByID/" + objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {



          $('#updateCameraID').val(objectID);

          $('#updateCameraName').val(element[1]);
          // $("#updateCameraURL").find("option:contains(" + element.url + ")").attr('selected', 'selected');
          $("#updateCameraURL").val(element[4]);
          $('#updateCameraGroup').val(element[2]);
          // $("#updateCameraServer").val(element.server);


          serverID = element[7]
          getServers(serverID);

          features = element.features

          gl_server = element.server
          server_ip = element[9] + ":" + element[10]

          getUpdateFeatures(features, objectID, server_ip);

          $("#updateCameraServer").find("option:contains(" + server_ip + ")").attr('selected', 'selected');



        })
      }
    });


  });

  $('#ModalUpdateCamera').on('show.bs.modal', function (e) {
    $("#updateFeature").html("");

  });

  $('#buttonCameraUpdate').click(function () {
    var updateOID = $('#ModalUpdateCamera').data('oid');
    var cameraName = $("#updateCameraName").val();
    var cameraURL = $("#updateCameraURL option:selected").val();
    var cameraURLName = $("#updateCameraURL option:selected").text();
    var cameraGroup = $("#updateCameraGroup option:selected").val();
    var cameraServer = $("#updateCameraServer option:selected").text();
    var cameraServerID = $("#updateCameraServer option:selected").val();


    getBoundary("");

    $.ajax({
      type: 'GET',

      url: database_url + "/feature/get",
      success: function (list) {
        var temp = [];
        var features = [];

        JSON.parse(list).forEach(element => {
          if ($('input#updateFeature' + element[0]).prop('checked') == true) {

            features.push(element[0]);
          }



        })

        var database_endpoint = database_url + '/camera/update';
        gl_server = cameraServer
        const data = {
          'object_id': updateOID,
          'camera_name': cameraName,
          'camera_stream': cameraURL,
          'camera_url_name': cameraURLName,
          'camera_group': cameraGroup,
          'camera_serverID': cameraServerID,
          'features': features,
          'user_id': user_id
        };

        fetch(database_endpoint, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then(response => {
            if (response.status == 422) {
              alert("Camera ID already exists")
            }
            location.reload();

          })
          .then(data => {


          })
          .catch((error) => {
            console.error('Error:', error);


          });
      }
    });

  });


  $('#ModalPresetCounting').on('hidden.bs.modal', function () {
    $(this).removeData('bs.modal');

  });

  $('#ModalPresetCounting').on('show.bs.modal', function (e) {
    gl_boundary_event = e
    var keys = $(e.relatedTarget).attr('data-id');

    str_keys = keys.split("_");
    cameraID = str_keys[0]
    serverIP = str_keys[1]
    featureID = str_keys[2]
    featureType = str_keys[3]

    document.getElementById('CameraID').value = cameraID;
    document.getElementById('serverIP').value = serverIP;
    document.getElementById('featureID').value = featureID;
    document.getElementById('featureType').value = featureType;

    
    
    $("#containerRowTest").empty();
    $("#containerRowTest").html(`<div id="containerRowTest"><div><img class="card-img-top" src="img/camera/${cameraID}.jpg" id="img_counting"
                                name= 'img_counting'></div></div>`);



    if (featureType == "jaywalking") {
      $("#exampleModalLabel_preset").html("Jaywalking Pre-set");

      
      $("#div_vehicle").css("display", "none");
      $("#div_pedestrian").css("display", "none");

      

    }
    else if (featureType == "vehicle") {
      $("#exampleModalLabel_preset").html("Vehicle and Pedestrian Counting Pre-set");

      $("#div_vehicle").css("display", "block");
      $("#div_pedestrian").css("display", "block");

      


    }

    getBoundary(featureType);






    


    $('#img_counting').click(function (e) {

      var offset_t = $(this).offset().top - $(window).scrollTop();
      var offset_l = $(this).offset().left - $(window).scrollLeft();
      w = $(this).prop("width");        // Width  (Rendered)
      h = $(this).prop("height");        // Height (Rendered)
      nw = $(this).prop("naturalWidth");  // Width  (Natural)
      nh = $(this).prop("naturalHeight"); // Height (Natural)
      var left = Math.round((e.clientX - offset_l));
      var top = Math.round((e.clientY - offset_t));
      x_data = Math.round((left * nw) / w);
      y_data = Math.round((top * nh) / h);


      var server_name = document.getElementById("CameraID").value;
      var laneName = document.getElementById("laneName").value;
      var flexType = $("input:radio[name=flexType]:checked").val()



      var polygon = document.getElementById("polygon").value;
      polygon += "(" + x_data + "," + y_data + ")"
      document.getElementById('polygon').value = polygon;



    });


    getLaneCounting(featureID);



  });

  $('#ModalPresetJaywalking').on('show.bs.modal', function (e) {
    gl_boundary_event = e
    var keys = $(e.relatedTarget).attr('data-id');

    str_keys = keys.split("_");
    cameraID = str_keys[0]
    serverIP = str_keys[1]

    document.getElementById('CameraID_jaywalking').value = cameraID;
    document.getElementById('serverIP_jaywalking').value = serverIP;

    

    getJaywalkingArea(cameraID);

    $("#containerJaywalkingImg").html(`<div id="containerJaywalkingImg"><div><img class="card-img-top" id="imgJaywalking${cameraID}"  src='http://${serverIP}/get_image_jaywalking_byID/${cameraID}'"></div></div>`);

    $('#imgJaywalking' + cameraID).click(function (e) {

      var offset_t = $(this).offset().top - $(window).scrollTop();
      var offset_l = $(this).offset().left - $(window).scrollLeft();
      w = $(this).prop("width");        // Width  (Rendered)
      h = $(this).prop("height");        // Height (Rendered)
      nw = $(this).prop("naturalWidth");  // Width  (Natural)
      nh = $(this).prop("naturalHeight"); // Height (Natural)
      var left = Math.round((e.clientX - offset_l));
      var top = Math.round((e.clientY - offset_t));
      x_data = Math.round((left * nw) / w);
      y_data = Math.round((top * nh) / h);


      var server_name = document.getElementById("CameraID_jaywalking").value;
      var areaName = document.getElementById("areaName").value;




      var polygon = document.getElementById("polygon_jaywalking").value;
      polygon += "(" + x_data + "," + y_data + ")"
      document.getElementById('polygon_jaywalking').value = polygon;




    });





  });

  $('#clearJaywalking').on('click', function (e) {
    document.getElementById('areaName').value = "";
    document.getElementById('polygon_jaywalking').value = "";
    var $status = $("#statusAddJaywalking");

    $status.css({ "color": "green" });
    $status.text("").removeClass("invisible");
  });

  $('#saveJaywalking').on('click', function (e) {
    var $status = $("#statusAddJaywalking");

    var cameraID = $("#CameraID_jaywalking").val();
    var areaName = $("#areaName").val();
    var serverIP = $("#serverIP_jaywalking").val();
    var polygon = $("#polygon_jaywalking").val();

    const str_polygon = polygon.split(')(');


    if (areaName == "") {
      $status.css({ "color": "red" });
      $status.text("Please fill out the area name").removeClass("invisible");
    }
    else if (polygon == "" || str_polygon.length < 3) {
      $status.css({ "color": "red" });
      $status.text("Please select at least three points to create a polygon").removeClass("invisible");
    }
    else {


      $status.css({ "color": "green" });
      $status.text("").removeClass("invisible");

      const data = {
        'camera_id': cameraID,
        'area_name': areaName,
        'polygon': polygon

      };



      $.ajax({
        type: 'POST',
        url: database_url + "/jaywalking_boundary/store",
        data: data,
        dataType: "text",
        success: function (data) {



          document.getElementById('areaName').value = "";
          document.getElementById('polygon_jaywalking').value = "";

          getJaywalkingArea(cameraID);
          // var el = document.getElementById('imgJaywalking'+cameraID);
          // el.remove();

          // // $("#containerJaywalkingImg").empty();
          // $("#containerJaywalkingImg").html(`<div id="containerJaywalkingImg"><div><img id="imgJaywalking${cameraID}" src='http://${serverIP}/get_image_jaywalking_byID/${cameraID}' class="img-fluid w-100 h-auto p-0 m-0"></div></div>`);






        },
        error: function (xhr, status, error) {

          if (xhr.status == 44) {
            $status.css({ "color": "red" });
            $status.text("Area Name already exists").removeClass("invisible");
          }



        }
      });
    }



  });

  $('#ModalDeleteJaywalking').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });


  //////////////////// Starting Trespassing //////////////////////
  $('#ModalPresetTrespassing').on('show.bs.modal', function (e) {
    gl_boundary_event = e
    var keys = $(e.relatedTarget).attr('data-id');

    str_keys = keys.split("_");
    cameraID = str_keys[0]
    serverIP = str_keys[1]

    document.getElementById('CameraID_trespassing').value = cameraID;
    document.getElementById('serverIP_trespassing').value = serverIP;


    getTrespassingArea(cameraID);

    $("#containerTrespassingImg").html(`<div id="containerTrespassingImg"><div><img class="card-img-top" id="imgTrespassing${cameraID}"  src='http://${serverIP}/get_image_trespassing_byID/${cameraID}'"></div></div>`);

    $('#imgTrespassing' + cameraID).click(function (e) {

      var offset_t = $(this).offset().top - $(window).scrollTop();
      var offset_l = $(this).offset().left - $(window).scrollLeft();
      w = $(this).prop("width");        // Width  (Rendered)
      h = $(this).prop("height");        // Height (Rendered)
      nw = $(this).prop("naturalWidth");  // Width  (Natural)
      nh = $(this).prop("naturalHeight"); // Height (Natural)
      var left = Math.round((e.clientX - offset_l));
      var top = Math.round((e.clientY - offset_t));
      x_data = Math.round((left * nw) / w);
      y_data = Math.round((top * nh) / h);


      var server_name = document.getElementById("CameraID_trespassing").value;
      var areaName = document.getElementById("areaName_trespassing").value;




      var polygon = document.getElementById("polygon_trespassing").value;
      polygon += "(" + x_data + "," + y_data + ")"
      document.getElementById('polygon_trespassing').value = polygon;




    });





  });

  $('#saveTrespassing').on('click', function (e) {
    var $status = $("#statusAddTrespassing");

    var cameraID = $("#CameraID_trespassing").val();
    var areaName = $("#areaName_trespassing").val();
    var serverIP = $("#serverIP_trespassing").val();
    var polygon = $("#polygon_trespassing").val();

    const str_polygon = polygon.split(')(');

    if (areaName == "") {
      $status.css({ "color": "red" });
      $status.text("Please fill out the area name").removeClass("invisible");
    }
    else if (polygon == "" || str_polygon.length < 3) {
      $status.css({ "color": "red" });
      $status.text("Please select at least three points to create a polygon").removeClass("invisible");
    }
    else {


      $status.css({ "color": "green" });
      $status.text("").removeClass("invisible");

      const data = {
        'camera_id': cameraID,
        'area_name': areaName,
        'polygon': polygon

      };



      $.ajax({
        type: 'POST',
        url: database_url + "/trespassing_boundary/store",
        data: data,
        dataType: "text",
        success: function (data) {



          document.getElementById('areaName').value = "";
          document.getElementById('polygon_trespassing').value = "";

          getTrespassingArea(cameraID);
          // var el = document.getElementById('imgJaywalking'+cameraID);
          // el.remove();

          // // $("#containerJaywalkingImg").empty();
          // $("#containerJaywalkingImg").html(`<div id="containerJaywalkingImg"><div><img id="imgJaywalking${cameraID}" src='http://${serverIP}/get_image_jaywalking_byID/${cameraID}' class="img-fluid w-100 h-auto p-0 m-0"></div></div>`);






        },
        error: function (xhr, status, error) {

          if (xhr.status == 44) {
            $status.css({ "color": "red" });
            $status.text("Area Name already exists").removeClass("invisible");
          }



        }
      });
    }



  });

  $('#ModalDeleteTrespassing').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteTrespassing').click(function () {
    var areaID = $('#ModalDeleteTrespassing').data('oid');


    $.ajax({
      type: 'DELETE',
      url: database_url + "/trespassing_boundary/delete/" + areaID,
      success: function (data) {
        var cameraID = document.getElementById("CameraID_trespassing").value
        getTrespassingArea(cameraID);
        $('#ModalDeleteTrespassing').modal('hide');

      }
    });



  });



  function getTrespassingArea(camera_id) {

    $("#showTrespassing").empty();

    $.ajax({
      type: 'GET',
      url: database_url + "/trespassing_boundary/get/" + camera_id,
      success: function (data) {

        JSON.parse(data).forEach((results, index) => {


          $("#showTrespassing").append("<tr><td>" + results.area_name + "</td><td>" +
            "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteTrespassing' id='buttonModalDeleteTrespassing'>Delete</a></td>" +

            + "</tr>")
        })
      }
    });
  }



  //////////////////// Ending Trespassing //////////////////////

  $('#buttonDeleteArea').click(function () {
    var areaID = $('#ModalDeleteJaywalking').data('oid');


    $.ajax({
      type: 'DELETE',
      url: database_url + "/jaywalking_boundary/delete/" + areaID,
      success: function (data) {
        var cameraID = document.getElementById("CameraID_jaywalking").value
        getJaywalkingArea(cameraID);
        $('#ModalDeleteJaywalking').modal('hide');

      }
    });



  });

  $('#clearVehicleCounting').on('click', function (e) {
    document.getElementById('laneName').value = "";
    document.getElementById('polygon').value = "";
    var $status = $("#statusAddCountingVehicle");

    $status.css({ "color": "green" });
    $status.text("").removeClass("invisible");

    var cameraID = $("#CameraID").val();
    var serverIP = $("#serverIP").val();
    var featureType = $("#featureType").val();

    


  });

  $('#saveVehicleCounting').on('click', function (e) {


    var $status = $("#statusAddCountingVehicle");
    var cameraID = $("#CameraID").val();
    var laneName = $("#laneName").val();
    var serverIP = $("#serverIP").val();
    var feature_id = $("#featureID").val();
    var feature_type = $("#featureType").val();
    var flexType = $("input[name='flexType']:checked").val();
    var polygon = $("#polygon").val();


    const str_polygon = polygon.split(')(');


    if (laneName == "") {
      $status.css({ "color": "red" });
      $status.text("Please fill out the lane name").removeClass("invisible");
    }
    else if (polygon == "" || str_polygon.length < 3) {
      $status.css({ "color": "red" });
      $status.text("Please select at least three points to create a polygon").removeClass("invisible");
    }
    else {


      $status.css({ "color": "green" });
      $status.text("").removeClass("invisible");

      if (feature_type != "vehicle") {
        flexType = feature_type;
      }



      const data = {
        'camera_feature_id': feature_id,
        'lane_name': laneName,
        'lane_type': flexType,
        'polygon': polygon,
        'user_id': user_id

      };


      $.ajax({
        type: 'POST',
        url: database_url + "/counting_boundary/store",
        data: data,
        dataType: "text",
        success: function (data) {



          document.getElementById('laneName').value = "";
          document.getElementById('polygon').value = "";


          getBoundary(feature_type);

          getLaneCounting(feature_id);





       


        },
        error: function (xhr, status, error) {

          if (xhr.status == 422) {
            $status.css({ "color": "red" });
            $status.text("Lane Name already exists").removeClass("invisible");
          }


        }
      });
    }



  });

  $('#buttonDeleteLane').click(function () {
    var laneID = $('#ModalDeleteLane').data('oid');
    var feature_id = $("#featureID").val();
    var feature_type = $("#feature_type").val();

    $.ajax({
      type: 'DELETE',
      url: database_url + "/counting_boundary/delete/" + laneID,
      success: function (data) {
        var cameraID = document.getElementById("CameraID").value
        getLaneCounting(feature_id);
        $('#ModalDeleteLane').modal('hide');





      }
    });



    getBoundary(feature_type);
  });

  $('#saveInfo').on('click', function (e) {
    var $status = $("#statusAdd");

    var cameraName = $("#inputCameraName").val();
    var cameraURL = $("#inputCameraURL option:selected").text();
    var cameraStream = $("#inputCameraURL option:selected").val();
    var cameraGroup = $("#inputCameraGroup option:selected").val();
    var cameraServer = $("#inputCameraServer option:selected").text();


    if (cameraName && cameraURL && cameraGroup && cameraServer) {

      var cameraName = $("#inputCameraName").val();
      var cameraURL = $("#inputCameraURL option:selected").val();
      var cameraURLName = $("#inputCameraURL option:selected").text();

      var cameraServer = $("#inputCameraServer option:selected").text();
      var cameraServerID = $("#inputCameraServer option:selected").val();
      var cameraGroup = $("#inputCameraGroup option:selected").val();
      var cameraGroupName = $("#inputCameraGroup option:selected").text();


      server_data = cameraServerID.split("_");
      server_id = server_data[0]
      server_ip_port = server_data[1]


      // create an XHR object
      var request = new XMLHttpRequest();
      var params = "UID=CORS&name=CORS";
      request.timeout = 5000;

      request.onreadystatechange = function () {



        //Connect to the server sucessfully
        if (request.readyState === 4) {
          if (request.status === 200) {
            $status.css({ "color": "green" });
            $status.text(" The server " + server_ip_port + " is connected").removeClass("invisible");

            //Add Data
            $.ajax({
              type: 'GET',
              url: database_url + "/feature/get_isActivate",
              success: function (list) {


                const data = {
                  'camera_name': cameraName,
                  'camera_stream': cameraStream,
                  'camera_url_name': cameraURLName,
                  'camera_group': cameraGroup,
                  'camera_server': cameraServerID,
                  'features': "",
                  'user_id': user_id,

                };

                fetch(database_url + '/camera/store', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(data),
                })
                  .then(response => {




                    if (response.status == 422) {

                      $status.css({ "color": "red" });
                      $status.text("Camera ID already exists").removeClass("invisible");
                    }





                    $("#saveInfo").css("display", "none");
                    $("#buttonCameraAdd").attr("disabled", false);
                    $('#features').removeClass('disabled');


                    $.ajax({
                      type: 'GET',
                      url: database_url + "/camera/getByName/" + cameraName + "_" + cameraStream,
                      success: function (data) {


                        JSON.parse(data).forEach(element => {


                          cameraServer = element[9] + ":" + element[10]

                          // getFeatures(element[0], cameraServer);

                          getUpdateFeatures("", element[0], cameraServer);

                          
                          $("#containerRow").empty();
                          $("#containerRow").html(`<div id="containerRow"><div><h4>${cameraName}</h4><img id="mainCam" src='http://${server_ip_port}/processed_stream/${element[0]}' class="img-fluid w-100 h-auto m-0 p-0"></div></div>`);



                        })
                      }
                    });

                    renderCards();

                    // var reloadcam = setInterval("ChangeMedia()",2000);



                  })
                  .then(data => {
                  })
                  .catch((error) => {

                  });



              }
            });


          }
          /// Cannot Connect to the server
          else {
            $status.css({ "color": "red" });
            $status.text(" Cannot connect to the server " + server_ip_port).removeClass("invisible");
          }
        }

        //Connecting to the server
        else if (request.readyState === 1) {
          $status.css({ "color": "orange" });
          $status.text(" Connecting to the server " + server_ip_port).removeClass("invisible");
        }


      };
     
      request.open('GET', "http://" + server_ip_port + "/test_camera_connection/"+cameraStream, true);
      // request.setRequestHeader('api-key', 'your-api-key');
      // request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      request.send(params);


    } else {

      if(cameraName== "")
      {
          $status.css({ "color": "red" });
          $status.text("Please fill out the camera name").removeClass("invisible");
      }
      else if(cameraURLName== "")
      {
          $status.css({ "color": "red" });
          $status.text("Please select the camera URL").removeClass("invisible");
      }
      else if(cameraServer== "")
      {
          $status.css({ "color": "red" });
          $status.text("Please select the camera name").removeClass("invisible");
      }
      else if(cameraGroupName== "")
      {
          $status.css({ "color": "red" });
          $status.text("Please select the camera group name").removeClass("invisible");
      }

    }
  });


  $('#saveNewInfo').on('click', function (e) {
    var cameraID = $("#updateCameraID").val();
    var cameraName = $("#updateCameraName").val();
    var cameraURL = $("#updateCameraURL option:selected").text();
    var cameraGroup = $("#updateCameraGroup option:selected").val();
    var cameraServer = $("#updateCameraServer option:selected").text();



    if (cameraName && cameraURL && cameraGroup && cameraServer) {
      $('#updateFeatures').removeClass('disabled');
      $('#updateTrespassing').attr('href', '/set_boundary/' + cameraID);
      $('#updateJaywalking').attr('href', '/set_jwalk_boundary/' + cameraID);
      $('#updateCounting').attr('href', '/set_counting_boundary/' + cameraID + "?server=" + cameraServer);
    } else {
      alert("Please fill out the require fields! (*)")
    }
  });


  $('#ModalSuspendCamera').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
    var keys = $('#ModalSuspendCamera').data('oid');
    str_keys = keys.split("_");
    cameraID = str_keys[0]
    suspend_status = str_keys[2]


    $("buttonSuspendCamera").addClass("btn btn-primary");


    if (suspend_status == "true") {
      $("#modalLabelSuspend").text("Activate Camera");
      $("#messageSuspend").text("Are you sure you want to activate this camera?");
      $("#buttonSuspendCamera").text("Activate Camera");




    }
    else {
      $("#modalLabelSuspend").text("Suspend Camera");
      $("#buttonSuspendCamera").text("Suspend Camera");
      $("#messageSuspend").text("Are you sure you want to suspend this camera?");
      // $("buttonSuspendCamera").removeClass("btn btn-danger");
      $("buttonSuspendCamera").addClass("btn btn-primary");
    }

    // $.ajax({
    //   type: 'DELETE',
    //   url: database_url + "/camera/delete/" + camID,
    //   success: function (data) {
    //     location.reload();
    //   }
    // });


  });


  $('#buttonSuspendCamera').click(function () {
    

    var keys = $('#ModalSuspendCamera').data('oid');
    str_keys = keys.split("_");
    cameraID = str_keys[0]
    server = str_keys[1]
    suspend_status = str_keys[2]
    
    const data = {
      'camera_id': cameraID,
      'suspend_status': suspend_status,
      'user_id': user_id,
      

    };

    $.ajax({
      type: 'POST',
      url: database_url + "/camera/setSuspend",
      data: data,
      dataType: "text",
      success: function (data) {
        location.reload();
      }
    });



    if (suspend_status == "false") {
      $.ajax({
        type: 'GET',
        dataType: 'json',
        url: "http://" + server + "/terminate_processed_thread",

        success: function (res) {

          // location.reload();

        }
      });

    }
    else {
      $.ajax({
        type: 'GET',
        dataType: 'json',
        url: "http://" + server + "/activate_processed_thread",

        success: function (res) {

          // location.reload();

        }
      });
    }


  });


  // $('#buttonSuspendCamera').click(function () {
  //   var camID = $('#ModalDeleteCamera').data('oid');

  //   // create an XHR object
  //   $.ajax({
  //     type: 'GET',
  //     dataType: 'json',
  //     url: "http://127.0.0.1:7001/terminate_processed_thread",

  //     success: function (res) {

  //       location.reload();

  //     }
  //   });


  // });



  /************** ADMIN **************/
  // let val;
  // let numOfFeatures;
  // // renderCards();

  // ******************************************* Camera **********************************
  // $('#buttonDeleteAllCamera').click(function () {
  //   $.ajax({
  //     type: 'DELETE',
  //     url: database_url + "/camera/deleteAll",
  //     dataType: "text",
  //     success: function (data) {
  //
  //     }
  //   });
  // });

  function getBoundary(count_type)
  {
    
    var cameraID = $("#CameraID").val();
    var serverIP = $("#serverIP").val();
    var dt = Date.now()
    var server = serverIP.split(":");
    var server_processing = server[0] +":6999"
    

    $.ajax({
      type: 'GET',
      url: "http://" + server_processing + "/draw_boundary_byID/" + cameraID+"?date_time="+dt+"&feature_type="+count_type,
      success: function (data) {




           $("#containerRowTest").empty();
           $("#containerRowTest").html(`<div id="containerRowTest"><div><img class="card-img-top" src="img/camera/${cameraID}_${dt}.jpg" id="img_counting" name= 'img_counting'></div></div>`);

            $('#img_counting').click(function (e) {

              var offset_t = $(this).offset().top - $(window).scrollTop();
              var offset_l = $(this).offset().left - $(window).scrollLeft();
              w = $(this).prop("width");        // Width  (Rendered)
              h = $(this).prop("height");        // Height (Rendered)
              nw = $(this).prop("naturalWidth");  // Width  (Natural)
              nh = $(this).prop("naturalHeight"); // Height (Natural)
              var left = Math.round((e.clientX - offset_l));
              var top = Math.round((e.clientY - offset_t));
              x_data = Math.round((left * nw) / w);
              y_data = Math.round((top * nh) / h);





              var polygon = document.getElementById("polygon").value;
              polygon += "(" + x_data + "," + y_data + ")"
              document.getElementById('polygon').value = polygon;






            });



      }
    });


    
  }

  function getFeatures(camera_id, serverIP) {


    // $.ajax({
    //   type: 'GET',
    //   url: database_url + "/feature/get_isActivate",
    //   success: function (data) {
    //     var temp = [];


    //     $("#inputFeature").empty();
    //     JSON.parse(data).forEach(function (element, index) {
    //       // USE FOR TABLE


    //       if (element[1].toLowerCase() == "trespassing") {
    //         //$("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-primary btn-sm' data-toggle='modal' data-target='#ModalPresetTrespassing' data-id='" + camera_id + "_" + serverIP +"_"+element[4]+ "' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
    //         $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + camera_id + "_" + serverIP + "_" + element[0] + "_trespassing' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")

    //       } else if (element[1].toLowerCase() == "jaywalking") {
    //         //$("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-primary btn-sm' data-toggle='modal' data-target='#ModalPresetJaywalking' data-id='" + camera_id + "_" + serverIP +"_"+element[4]+"' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
    //         $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + camera_id + "_" + serverIP + "_" + element[0] + "_jaywalking' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")

    //       } else if (element[1].toLowerCase() == "vehicle counting") {


    //         // $("#inputFeature").append("<a id='edit" + element._id.$oid + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + camera_id + "_" + serverIP + "' type='button' class='btn btn-info btn-sm'>artty</a>")
    //         $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + 
    //         "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td><a id='edit" + 
    //         element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + 
    //         camera_id + "_" + serverIP + "_" + element[0] + "_vehicle' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")

    //       }
    //       else {

    //         $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='" + element[0] + "' value=" + element[1] + "></input></td><td></td></tr>")


    //       }
    //     })
    //   }
    // });
  }

  function getUpdateFeatures(features, objectID, serverIP) {

    
    $("#inputFeature").html("");
    $("#updateFeature").html("");

    $.ajax({
      type: 'GET',
      url: database_url + "/camera_feature/getByID/" + objectID,
      success: function (data) {
        var temp = [];


        JSON.parse(data).forEach(function (element, index) {
          // USE FOR TABLE

          
          str_check = "unchecked";


          if (element[6] == true) {
            str_check = "checked";


          }


          

          if (element[1] == "trespassing") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='inputFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='inputFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_trespassing' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_trespassing' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")

            //$("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + elementp[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='update" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetTrespassing' data-id='" + element[4] + "_" + serverIP +"_"+element[4]+ "' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")
          } else if (element[1] == "jaywalking") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='inputFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='inputFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_jaywalking' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_jaywalking' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")


            //$("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='update" + element[0]  + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetJaywalking' data-id='" + element[4] + "_" + serverIP +"_"+element[4]+"' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")
          } else if (element[1] == "vehicle counting") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='inputFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='inputFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_vehicle' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td><a id='edit" + element[0] + " class='isAdmin btn btn-success btn-sm' data-toggle='modal' data-target='#ModalPresetCounting' data-id='" + objectID + "_" + serverIP + "_" + element[4] + "_vehicle' type='button' class='btn btn-info btn-sm'>pre-set</a></td></tr>")
          }
          else {

            $("#inputFeature").append("<tr><td><label class='form-check-label' for='inputFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='inputFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td></td></tr>")
            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element[0] + "'>" + element[1] + "</label></td><td><input type='checkbox' id='updateFeature" + element[0] + "' value=" + element[1] + " " + str_check + "></input></td><td></td></tr>")

          }

        })

      }
    });
  }

  function getJaywalkingArea(camera_id) {

    $("#showJaywalking").empty();

    $.ajax({
      type: 'GET',
      url: database_url + "/jaywalking_boundary/get/" + camera_id,
      success: function (data) {

        JSON.parse(data).forEach((results, index) => {


          $("#showJaywalking").append("<tr><td>" + results.area_name + "</td><td>" +
            "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteJaywalking' id='buttonModalDeleteJaywalking'>Delete</a></td>" +

            + "</tr>")
        })
      }
    });
  }




  function getLaneCounting(feature_id) {

    $("#showCounting").empty();


    $.ajax({
      type: 'GET',
      url: database_url + "/counting_boundary/get/" + feature_id,
      success: function (data) {

        JSON.parse(data).forEach((results, index) => {


          $("#showCounting").append("<tr><td>" + results[2] + "</td><td>" +
            results[6] + "</td><td >" +

            "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteLane' id='buttonModalDeleteLane'>Delete</a></td>" +

            + "</tr>")
        })
      }
    });
  }


  function getCameraStreams() {
    $.ajax({
      type: 'GET',
      url: database_url + "/camera_stream/get",
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        JSON.parse(data).forEach(function (element, index) {

          temp1.push("</div><option value=" + element[0] + ">" + element[2] + "</option></div>");
        });
        $('#inputCameraURL').html(temp1);
        $('#updateCameraURL').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }



  function getServers(serverID) {

    $('#inputCameraServer').empty();
    $('#updateCameraServer').empty();

    $.ajax({
      type: 'GET',
      url: database_url + "/server/get_activate/"+serverID,
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];


        JSON.parse(data).forEach(function (element, index) {

          str_select = "";
          if(element[0]  == serverID)
          {
            str_select = "selected='selected' "
          }
          temp1.push("</div><option value=" + element[0] + "_" + element[4] + ":" + element[5] + " "+str_select+">" + element[3] + "</option></div>");
        });
        $('#inputCameraServer').html(temp1);
        $('#updateCameraServer').html(temp1);


      }
    });
  }


  function renderCards(isValid) {
    $.ajax({
      type: 'GET',
      url: database_url + "/camera_group/get_activate/0",
      success: function (data) {


        var temp = [];
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        JSON.parse(data).forEach(function (element, index) {
          temp.push(
            `<div class="card">
                  <div class="card-header" id="headingOne">
                    <h2 class="mb-0">
                      <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#${element[0]}" aria-expanded="true" aria-controls="${element[0]}">
                        ${element[1]}
                      </button>
                    </h2>
                </div>

                <div id="${element[0]}" class="collapse container-fluid cardView" aria-labelledby="headingOne" data-parent="#accordionExample">
                </div>
              </div>`
          );
          temp1.push("</div><option value=" + element[0] + ">" + element[1] + "</option></div>");

        });
        $('#groupList').html(temp);
        $('#inputCameraGroup').html(temp1);
        $('#updateCameraGroup').html(temp1);

        // $('#updateCameraGroup').html(temp1);

        // $('#inputCameraGroup').val("0");

        $.ajax({
          type: 'GET',
          url: database_url + "/camera/get",
          success: function (data) {
            JSON.parse(data).forEach((results, index) => {
              suspendd_flag = "false"
              server_port = results[9] + ":" + results[10]
              str_suspended = '<a id="del' + results[0] + '" class="isAdmin btn btn-success  btn-sm" data-toggle="modal" data-target="#ModalSuspendCamera" data-id="' + results[0] + "_" + server_port + '_' + suspendd_flag + '" title="Click for Suspension" >Suspend</a>';
              str_img = "";





              str_disable = "disabled";
              if (user_type == "admin") {
                str_disable = ""
              }
              
              if (results[11] == true) {
                str_img = " disabled";
                suspendd_flag = "true"
                
                str_suspended = '<a id="del' + results[0] + '" class="isAdmin btn btn-secondary  btn-sm" data-toggle="modal" data-target="#ModalSuspendCamera" data-id="' + results[0] + "_" + server_port + '_' + suspendd_flag + '" title="Click for Activation" >Activate</a>'
              }

              

              // <img class= "card-img-top ${str_img}" id="img${results[0]}"  src="http://${server_port}/stream/${results[0]}" ></img>
              if (results[12] == true) {
                $("#containerRow").html(`<div id="containerRow"><div><h4>${results[1]} </h4><img id="mainCam" src='http://${server_port}/stream/${results[0]}'  class="img-fluid w-100 h-auto m-0 p-0 ${str_img}"; ></div></div>`);
              }


              $('#' + results[2]).append(
                `<div class="card" id="c${results[0]}" style="width: 18rem;">




                     <img src="img/stream/${results[4]}.jpg" id="img${results[0]}">
                      <div id="cameras" class="card-body">
                        <h5 class="card-title">${results[1]}</h5>
                        <p class="card-text"></p>

                        <a id="edit${results[0]}" class="isAdmin btn btn-primary ${str_disable} btn-sm" data-toggle="modal" data-target="#ModalUpdateCamera" data-id="${results[0]}">Edit</a>
                        <a id="del${results[0]}" class="isAdmin btn btn-danger ${str_disable}  btn-sm" data-toggle="modal" data-target="#ModalDeleteCamera" data-id="${results[0]}_${server_port}">Delete</a>
                        ${str_suspended}

                      </div>
                    </div>`
              );




              $('#img' + results[0]).click(function () {
                server_port = results[9] + ":" + results[10]

                $("#containerRow").html(`  <div id="containerRow"><div><h4>${results[1]}</h4><img id="mainCam" src='http://${server_port}/stream/${results[0]}' class="img-fluid w-100 h-auto m-0 p-0"></div></div>`);
                var database_endpoint = database_url + '/camera/setActive';

                const data = {
                  'object_id': results[0],
                  'user_id': user_id
                };
                fetch(database_endpoint, {
                  method: 'PUT',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(data),
                })



              });

              // $('#set' + results[0]).click(function () {
              //   $("#containerRow").html(`<div id="containerRow"><div><h4>${results.name}</h4><img id="mainCam" src='http://${server_port}/main_stream/${results[0]}' class="img-fluid w-100 h-auto m-0 p-0 ${str_img}"></div></div>`);
              //   var database_endpoint = database_url + '/camera/setActive';

              //   const data = {
              //     'object_id': results[0],
              //     'user_id': user_id
              //   };
              //   fetch(database_endpoint, {
              //     method: 'PUT',
              //     headers: {
              //       'Content-Type': 'application/json',
              //     },
              //     body: JSON.stringify(data),
              //   })
              // });

              $('#del' + results[0]).click(function () {
                val = results[0];



              });
            });
          }
        })
      }
    });


  }

  $(document).on('click', '.card-img-top', function () {
    imgsrc = $(this).attr('src');
    $("#img-focus").attr('src', imgsrc);
  });
});

function ChangeMedia() {

}
