$(document).ready(function () {

  $('#buttonAreaAdd').click(function () {

    var $status = $("#statusAdd");
    var areaName = $("#inputAreaName").val();
    var areaAddress = $("#inputAreaAddress").val();

    
    if (areaName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Area Name.').removeClass("invisible");
    }
    else {
      // save area information in database
      const data = {
        'area_name': areaName.toLowerCase().trim(),
        'area_address': areaAddress,
        'user_id': user_id

      };

      $.ajax({
        type: 'POST',
        url: database_url + "/camera_area/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
          // renderCards(true);
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text('Area name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
        
      });
    }
  });

  $('#buttonCamAreaUpdate').click(function () {
    var $status = $("#statusUpdate");
    var updateOID = $('#ModalUpdateCamArea').data('oid');
    var areaName = $("#updateAreaName").val().trim();
    var areaAddress = $("#updateAreaAddress").val();

    
    if (areaName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Area Name.').removeClass("invisible");
    }
    else {
      // save area information in database
      const data = {
        'object_id': updateOID,
        'area_name': areaName.toLowerCase().trim(),
        'area_address': areaAddress,
        'user_id':user_id
      };

      $.ajax({
        type: 'PUT',
        url: database_url + "/camera_area/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text('Area name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#ModalUpdateCamArea').on('show.bs.modal', function (e) {


    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/camera_area/getByID/"+objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {
          
            console.log(element.server);
            $('#updateAreaName').val(element[1]);
            $('#updateAreaAddress').val(element[2]);

          
        })
      }
    });

  });

  $('#buttonCamAreaActivate').click(function () {
    var updateOID = $('#ModalActivateCamArea').data('oid');

  

    $.ajax({
      type: 'POST',
      url: database_url + "/camera_area/activate/" + updateOID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateCamArea').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalDeleteCamArea').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteCamArea').click(function () {
    var camID = $('#ModalDeleteCamArea').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/camera_area/delete/" + camID,
      success: function (data) {
        
        location.reload();
      },
      error: function (data) {
        var $status = $("#statusDelete");
        if(data.responseText == "ForeignKey")
        {
          $status.css({ "color": "red" });
          $status.text('The data cannot be deleted because references to this key still exist ').removeClass("invisible");
        }
        
        
    
        
      }

    });
  });


  $.ajax({
    type: 'GET',
    url: database_url + "/camera_area/get",
    success: function (data) {
      
      JSON.parse(data).forEach((results, index) => {
        console.log(results[3] )
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateCamArea' id='buttonModalActivateCamArea' title='Click for Activation'>Activate</a></td>"
        if (results[3] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateCamArea' id='buttonModalActivateCamArea' title='Click for Inactivation' >Inactivate</a></td>"
        }


        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          results[2] + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateCamArea' id='buttonModalUpdateCamArea'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteCamArea' id='buttonModalDeleteCamArea'>Delete</a></td><td>" +
          str_activate+"</tr>")
      })
    }
  })

});
