$(document).ready(function () {

  $('#buttonServerTypeAdd').click(function () {

    var $status = $("#statusAdd");
    var serverTypeName = $("#inputServerTypeName").val();

    if (serverTypeName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Type Name.').removeClass("invisible");
    }
    else {
      // save group information in database

      
      const data = {
        'server_type_name': serverTypeName.toLowerCase().trim(),
        'user_id':user_id
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/server_type/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
          // renderCards(true);
        },
        error: function (data) {
          
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text('Server Type name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
        
      });
    }
  });

  $('#buttonServerTypeUpdate').click(function () {
    var $status = $("#statusUpdate");
    var updateOID = $('#ModalUpdateServerType').data('oid');
    var serverTypeName = $("#updateServerTypeName").val();

    
    if (serverTypeName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Server Type Name.').removeClass("invisible");
    }
    else {
      // save ServerType information in database
      const data = {
        'object_id': updateOID,
        'server_type_name': serverTypeName.toLowerCase().trim(),
        'user_id':user_id
      };

      $.ajax({
        type: 'PUT',
        url: database_url + "/server_type/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text('Server Type name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#ModalUpdateServerType').on('show.bs.modal', function (e) {


    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/server_type/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          if (element[0] == objectID) {
            console.log(element.server);
            $('#updateServerTypeName').val(element[1]);

          }
        })
      }
    });

  });

  $('#buttonServerTypeActivate').click(function () {
    var updateOID = $('#ModalActivateServerType').data('oid');

    console.log("my id: "+updateOID);

    $.ajax({
      type: 'POST',
      url: database_url + "/server_type/activate/" + updateOID+"_"+user_id,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateServerType').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalDeleteServerType').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteServerType').click(function () {
    var camID = $('#ModalDeleteServerType').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/server_type/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $.ajax({
    type: 'GET',
    url: database_url + "/server_type/get",
    success: function (data) {
      
      JSON.parse(data).forEach((results, index) => {
        
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateServerType' id='buttonModalActivateCamGroup' title='Click for Inactivation'>Activate</a></td>"
        if (results[2] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateServerType' id='buttonModalActivateCamGroup' title='Click for Activation' >Inactivate</a></td>"
        }


        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateServerType' id='buttonModalUpdateServerType'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteServerType' id='buttonModalDeleteServerType'>Delete</a></td><td>" +
          str_activate+"</tr>")
      })
    }
  })

});
