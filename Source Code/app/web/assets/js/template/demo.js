$(document).ready(function () {

  renderCards();
  getServers();
  getCameraStreams();


  $('#buttonCameraAdd').click(function () {
    $("#ModalAddCamera").modal('hide')
    var updateOID = $('#ModalUpdateCamera').data('oid');
    var cameraName = $("#inputCameraName").val();
    var cameraURL = $("#inputCameraURL option:selected").text();;

    
    var cameraServer = $("#inputCameraServer option:selected").text();
    var cameraGroup = $("#inputCameraGroup option:selected").val();


    $.ajax({
      type: 'GET',
      url: database_url + "/demo/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          if (element.name == cameraName && element.url == cameraURL) {
            console.log(element.server);
            $('#updateCameraName').val(element.name);
            $('#updateCameraURL option:selected').text(element.url);
            $('#updateCameraGroup').val(element.group);
            $("#updateCameraServer option:selected").text(element.server);


            updateOID = element._id.$oid
          }
        })
      }
    });


    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get_isActivate",
      success: function (list) {
        var temp = [];
        var features = [];

        JSON.parse(list).forEach(element => {
          if ($('input#' + element._id.$oid).prop('checked') == true) {
            var feature = { [element.feature_name]: $('input#' + element._id.$oid).prop('checked') }
            features.push(feature);
          }






        })

        console.log("Obj ID " + updateOID)
        //Update the Feature and Camera Location

        
        var database_endpoint = database_url + '/demo/update';
        const data = {
          'object_id': updateOID,
          'camera_name': cameraName,
          'camera_url': cameraURL,
          'camera_group': cameraGroup,
          'camera_server': cameraServer,
          // 'camera_latitude': lat,
          // 'camera_longitude': lng,
          'features': features
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
            location
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });






      }
    });
    renderCards();
  });

  $('#buttonCameraUpdate').click(function () {
    var updateOID = $('#ModalUpdateCamera').data('oid');
    var cameraName = $("#updateCameraName").val();
    var cameraURL = $("#updateCameraURL option:selected").text();
    var cameraGroup = $("#updateCameraGroup option:selected").val();
    var cameraServer = $("#updateCameraServer option:selected").text();


    $.ajax({
      type: 'GET',

      url: database_url + "/feature/get",
      success: function (list) {
        var temp = [];
        var features = [];

        JSON.parse(list).forEach(element => {
          if ($('input#updateFeature' + element._id.$oid).prop('checked') == true) {
            var feature = { [element.feature_name]: $('input#updateFeature' + element._id.$oid).prop('checked') }
            features.push(feature);
          }

          console.log(features)

        })

        var database_endpoint = database_url + '/demo/update';
        const data = {
          'object_id': updateOID,
          'camera_name': cameraName,
          'camera_url': cameraURL,
          'camera_group': cameraGroup,
          'camera_server': cameraServer,
          // 'camera_latitude': lat,
          // 'camera_longitude': lng,
          'features': features
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
            location
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }
    });
  });




  $('#ModalDeleteCamera').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

  });

  $('#buttonDeleteCamera').click(function () {
    var camID = $('#ModalDeleteCamera').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/demo/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });

  $('#ModalAddCamera').on('show.bs.modal', function (e) {
    $("#inputFeature").html("");

    console.log("==============> click ")
    getFeatures("123");




  });

  $('#ModalUpdateCamera').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id');
    $(this).data("oid", objectID);

    $.ajax({
      type: 'GET',
      url: database_url + "/demo/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          if (element._id.$oid == objectID) {
            console.log(element.server);
            $('#updateCameraID').val(objectID);

            $('#updateCameraName').val(element.name);
            $('#updateCameraURL option:selected').text(element.url);
            $('#updateCameraGroup').val(element.group);
            $("#updateCameraServer option:selected").text(element.server);

            features = element.features

            getUpdateFeatures(features,objectID);
            

          }
        })
      }
    });


  });

  $('#ModalUpdateCamera').on('show.bs.modal', function (e) {
    $("#updateFeature").html("");

  });

  $('#saveInfo').on('click', function (e) {
    var cameraName = $("#inputCameraName").val();
    var cameraURL = $("#inputCameraURL option:selected").text();
    var cameraGroup = $("#inputCameraGroup option:selected").val();
    var cameraServer = $("#inputCameraServer option:selected").text();


    if (cameraName && cameraURL && cameraGroup && cameraServer) {

      var cameraName = $("#inputCameraName").val();
      var cameraURL = $("#inputCameraURL option:selected").text();

      var cameraServer = $("#inputCameraServer option:selected").text();
      var cameraGroup = $("#inputCameraGroup option:selected").val();
      $.ajax({
        type: 'GET',
        url: database_url + "/feature/get_isActivate",
        success: function (list) {


          const data = {
            'camera_name': cameraName,
            'camera_url': cameraURL,
            'camera_group': cameraGroup,
            'camera_server': cameraServer,
            // 'camera_latitude': 0,
            // 'camera_longitude': 0,
            'features': ""

          };

          fetch(database_url + '/demo/store', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
            .then(response => {
              if (response.status == 422) {
                alert("Camera ID already exists")
              }

              $.ajax({
                type: 'GET',
                url: database_url + "/demo/get",
                success: function (data) {
                  JSON.parse(data).forEach(element => {
                    if (element.name == cameraName && element.url == cameraURL) {
                      console.log(element.server);

                      getFeatures(element._id.$oid);

                      $('#features').removeClass('disabled');
                      $('#setTrespassing').attr('href', '/set_video_boundary/' + element._id.$oid);
                      $('#setJaywalking').attr('href', '/set_jwalk_video_boundary/' + element._id.$oid);
                      $('#setCounting').attr('href', '/set_counting_video_boundary/' + element._id.$oid);

                      console.log("=====element._id.$oid=>" + element._id.$oid)

                    }
                  })
                }
              });


            })
            .then(data => {
            })
            .catch((error) => {
              console.log(error);
            });


        }
      });





    } else {
      alert("Please fill out the require fields! (*)")
    }
  });

  $('#saveNewInfo').on('click', function (e) {
    var cameraID = $("#updateCameraID").val();
    var cameraName = $("#updateCameraName").val();
    var cameraURL = $("#updateCameraURL option:selected").text();
    var cameraGroup = $("#updateCameraGroup option:selected").val();
    var cameraServer = $("#updateCameraServer option:selected").text();

    console.log("=<" + cameraID)
    if (cameraName && cameraURL && cameraGroup && cameraServer) {
      $('#updateFeatures').removeClass('disabled');
      $('#updateTrespassing').attr('href', '/set_video_boundary/' + cameraID);
      $('#updateJaywalking').attr('href', '/set_jwalk_video_boundary/' + cameraID);
      $('#updateCounting').attr('href', '/set_counting_video_boundary/' + cameraID);
    } else {
      alert("Please fill out the require fields! (*)")
    }
  });

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
  //       console.log("Cameras deleted");
  //     }
  //   });
  // });

  function getFeatures(camera_id) {
    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get_isActivate",
      success: function (data) {
        var temp = [];
        $("#inputFeature").empty();
        JSON.parse(data).forEach(function (element, index) {
          // USE FOR TABLE

          if (element.feature_name == "trespassing") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='" + element._id.$oid + "' value=" + element.feature_name + "></input></td><td><a id=set" + element.feature_name + " href='/set_video_boundary/" + camera_id + "' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")

          } else if (element.feature_name == "jaywalking") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='" + element._id.$oid + "' value=" + element.feature_name + "></input></td><td><a id=set" + element.feature_name + " href='/set_jwalk_video_boundary/" + camera_id + "' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")

          } else if (element.feature_name == "counting") {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='" + element._id.$oid + "' value=" + element.feature_name + "></input></td><td><a id=set" + element.feature_name + " href='/set_counting_video_boundary/" + camera_id + "' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")

          }
          else {
            $("#inputFeature").append("<tr><td><label class='form-check-label' for='feature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='" + element._id.$oid + "' value=" + element.feature_name + "></input></td><td></td></tr>")


          }
        })
      }
    });
  }

  function getUpdateFeatures(features,objectID) {
    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get_isActivate",
      success: function (data) {
        var temp = [];
        JSON.parse(data).forEach(function (element, index) {
          // USE FOR TABLE
          str_check = "unchecked";


          if (JSON.stringify(features).indexOf(element.feature_name) != -1) {
            str_check = "checked";


          }



          if (element.feature_name == "trespassing") {

            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='updateFeature" + element._id.$oid + "' value=" + element.feature_name + " " + str_check + "></input></td><td><a id=update" + element.feature_name + " href='/set_video_boundary/"+objectID+"' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")
          } else if (element.feature_name == "jaywalking") {

            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='updateFeature" + element._id.$oid + "' value=" + element.feature_name + " " + str_check + "></input></td><td><a id=update" + element.feature_name + " href='/set_jwalk_video_boundary/"+objectID+"' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")
          } else if (element.feature_name == "counting") {

            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='updateFeature" + element._id.$oid + "' value=" + element.feature_name + " " + str_check + "></input></td><td><a id=update" + element.feature_name + " href='/set_counting_video_boundary/"+objectID+"' target='_blank' type='button' class='btn btn-info btn-sm'>Pre-Set</a></td></tr>")
          }
          else {

            $("#updateFeature").append("<tr><td><label class='form-check-label' for='updateFeature" + element._id.$oid + "'>" + element.feature_name + "</label></td><td><input type='checkbox' id='updateFeature" + element._id.$oid + "' value=" + element.feature_name + " " + str_check + "></input></td><td></td></tr>")

          }

        })

      }
    });
  }


  function getCameraStreams() {
    $.ajax({
      type: 'GET',
      url: database_url + "/video/get",
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element._id.$oid + ">" + element.name + "</option></div>");
        });
        $('#inputCameraURL').html(temp1);
        $('#updateCameraURL').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }

  function getServers() {
    $.ajax({
      type: 'GET',
      url: database_url + "/server/get_activate",
      success: function (data) {
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        JSON.parse(data).forEach(function (element, index) {
          temp1.push("</div><option value=" + element._id.$oid + ">" + element.server_ip + ":" + element.server_port + "</option></div>");
        });
        $('#inputCameraServer').html(temp1);
        $('#updateCameraServer').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }


  function renderCards(isValid) {
    $.ajax({
      type: 'GET',
      url: database_url + "/demo_group/get_activate",
      success: function (data) {

        // JSON.parse(data).forEach(function (item, index) {
        //   console.log(item, index);
        // });

        var temp = [];
        // var temp1 = ["<option value='0'>Unlisted</div>"];
        var temp1 = [];
        JSON.parse(data).forEach(function (element, index) {
          temp.push(
            `<div class="card">
                  <div class="card-header" id="headingOne">
                    <h2 class="mb-0">
                      <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#${element._id.$oid}" aria-expanded="true" aria-controls="${element._id.$oid}">
                        ${element.name}
                      </button>
                    </h2>
                </div>

                <div id="${element._id.$oid}" class="collapse container-fluid cardView" aria-labelledby="headingOne" data-parent="#accordionExample">
                </div>
              </div>`
          );
          temp1.push("</div><option value=" + element._id.$oid + ">" + element.name + "</option></div>");

        });
        $('#groupList').html(temp);
        $('#inputCameraGroup').html(temp1);
        $('#updateCameraGroup').html(temp1);

        // $('#updateCameraGroup').html(temp1);

        // $('#inputCameraGroup').val("0");

        $.ajax({
          type: 'GET',
          url: database_url + "/demo/get",
          success: function (data) {
            JSON.parse(data).forEach((results, index) => {
              console.log(results.group);
              $('#' + results.group).append(
                `<div class="card" id="c${results._id.$oid}" style="width: 18rem;">
                  
                    <img class="card-img-top" id="img${results._id.$oid}"  src='http://${results.server}/stream/${results._id.$oid}' ">
                    
                      <div id="cameras" class="card-body">
                        <h5 class="card-title">${results.name}</h5>
                        <p class="card-text"></p>
                        <a id="set${results._id.$oid}" class="btn btn-primary btn-sm">Set</a>
                        <a id="edit${results._id.$oid}" class="isAdmin btn btn-success btn-sm" data-toggle="modal" data-target="#ModalUpdateCamera" data-id="${results._id.$oid}">Edit</a>
                        <a id="del${results._id.$oid}" class="isAdmin btn btn-danger btn-sm" data-toggle="modal" data-target="#ModalDeleteCamera" data-id="${results._id.$oid}">Delete</a>
                      </div>
                    </div>`
              );

              if (results.active == true) {
                $("#containerRow").html(`<div id="containerRow"><div><h4>${results.name} </h4><img id="mainCam" src='http://${results.server}/processed_stream/${results._id.$oid}'  class="img-fluid w-100 h-auto m-0 p-0"; ></div></div>`);
              }
              $('#img' + results._id.$oid).click(function () {
                $("#containerRow").html(`<div id="containerRow"><div><h4>${results.name}</h4><img id="mainCam" src='http://${results.server}/processed_stream/${results._id.$oid}' class="img-fluid w-100 h-auto m-0 p-0"></div></div>`);
                var database_endpoint = database_url + '/demo/setActive';
                console.log("======>" + results.url)
                const data = {
                  'object_id': results._id.$oid,
                  'active': true
                };
                fetch(database_endpoint, {
                  method: 'PUT',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(data),
                })
              });
              $('#set' + results._id.$oid).click(function () {
                $("#containerRow").html(`<div id="containerRow"><div><h4>${results.name}</h4><img id="mainCam" src='http://${results.server}/processed_stream/${results._id.$oid}' class="img-fluid w-100 h-auto m-0 p-0"></div></div>`);
                var database_endpoint = database_url + '/demo/setActive';

                const data = {
                  'object_id': results._id.$oid,
                  'active': true
                };
                fetch(database_endpoint, {
                  method: 'PUT',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(data),
                })

                location.reload();

              });

              $('#del' + results._id.$oid).click(function () {
                val = results._id.$oid;



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

function imagefun() {
  console.log("===>");
}