//Select Contact
$(document).ready(function () {

  $('#buttonRouteAdd').click(function () {
    var $status = $("#statusAdd");
    //   var routeServer = $("#inputRouteServer").val();
    var routeServer = $("#inputRouteServer option:selected").text();
    var routeFrom = $("#inputRouteFrom").val();
    var routeTo = $("#inputRouteTo").val();

    if (routeServer == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Lane Server.').removeClass("invisible");
    }
    else if (routeFrom == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter From.').removeClass("invisible");
    }
    else if (routeTo == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter To.').removeClass("invisible");
    }
    else {

      // save group information in database
      const data = {
        'routeServer': routeServer,
        'routeFrom': routeFrom,
        'routeTo': routeTo
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/lane/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          if( data.status == 44 ){
            $status.css({ "color": "red" });
            $status.text('"From" and "To" lane already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#buttonRouteUpdate').click(function () {
    var $status = $("#statusUpdate");
    var updateOID = $('#ModalUpdateRoute').data('oid');
    //   var routeServer = $("#updateRouteServer").val();
    var routeServer = $("#updateRouteServer option:selected").text();
    var routeFrom = $("#updateRouteFrom").val();
    var routeTo = $("#updateRouteTo").val();

    if (routeServer == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Lane Server.').removeClass("invisible");
    }
    else if (routeFrom == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter From.').removeClass("invisible");
    }
    else if (routeTo == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter To.').removeClass("invisible");
    }
    else {

    // save group information in database
    const data = {
      'object_id': updateOID,
      'routeServer': routeServer,
      'routeFrom': routeFrom,
      'routeTo': routeTo
    };

    $.ajax({
      type: 'PUT',
      url: database_url + "/lane/update",
      data: data,
      dataType: "text",
      success: function (data) {
        location.reload();
      },
      error: function (data) {
        alert("Please check all fields.");
      }
    });
  }
  });

  $('#ModalUpdateRoute').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/lane/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          if (element._id.$oid == objectID) {
            console.log(element.server);
            //   $('#updateRouteServer').val(element.server);
            $('#updateRouteFrom').val(element.from);
            $('#updateRouteTo').val(element.to);
          }
        })
      }
    });
  });

  $('#buttonLaneActivate').click(function () {
    var updateOID = $('#ModalActivateLane').data('oid');


    $.ajax({
      type: 'POST',
      url: database_url + "/lane/activate/" + updateOID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateLane').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });


  $('#ModalDeleteRoute').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteRoute').click(function () {
    var camID = $('#ModalDeleteRoute').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/lane/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });

  $.ajax({
    type: 'GET',
    url: database_url + "/lane/get",
    success: function (data) {
      console.log(data)


      JSON.parse(data).forEach((results, index) => {

        var str_activate = "<td> <a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateLane' id='buttonModalActivateLane' title='Click for Activate'>Inactivated</a></td>"
        if (results.lane_activate == "true") {
          str_activate = "<td> <a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateLane' id='buttonModalActivateLane' title='Click for Inactivate'>Activated</a></td>"
        }


        $("#showContact").append("<tr><td>" + results.server + "</td><td>" +
          results.from + "</td><td>" +
          results.to + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalUpdateRoute' id='buttonModalUpdateRoute'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteRoute' id='buttonModalDeleteRoute'>Delete</a></td>" +
          str_activate+"</tr>")
      })
    }
  })

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
        $('#inputRouteServer').html(temp1);
        $('#updateRouteServer').html(temp1);
        // $('#inputCameraServer').val("0");
      }
    });
  }
  getServers();

});