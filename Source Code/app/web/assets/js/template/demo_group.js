$(document).ready(function () {

  $('#buttonGroupAdd').click(function () {

    var $status = $("#statusAdd");
    var groupName = $("#inputGroupName").val();

    if (groupName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Group Name.').removeClass("invisible");
    }
    else {
      // save group information in database
      const data = {
        'group_name': groupName.toLowerCase().trim()
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/demo_group/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
          // renderCards(true);
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 44 ){
            $status.css({ "color": "red" });
            $status.text('Group name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
        
      });
    }
  });

  $('#buttonCamGroupUpdate').click(function () {
    var $status = $("#statusUpdate");
    var updateOID = $('#ModalUpdateCamGroup').data('oid');
    var groupName = $("#updateGroupName").val();
    if (groupName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Group Name.').removeClass("invisible");
    }
    else {
      // save group information in database
      const data = {
        'object_id': updateOID,
        'group_name': groupName.toLowerCase().trim()
      };

      $.ajax({
        type: 'PUT',
        url: database_url + "/demo_group/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 44 ){
            $status.css({ "color": "red" });
            $status.text('Group name already exists.').removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#ModalUpdateCamGroup').on('show.bs.modal', function (e) {


    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/demo_group/get",
      success: function (data) {
        JSON.parse(data).forEach(element => {
          if (element._id.$oid == objectID) {
            console.log(element.server);
            $('#updateGroupName').val(element.name);

          }
        })
      }
    });

  });

  $('#buttonCamGroupActivate').click(function () {
    var updateOID = $('#ModalActivateCamGroup').data('oid');

    
    $.ajax({
      type: 'POST',
      url: database_url + "/demo_group/activate/" + updateOID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateCamGroup').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalDeleteCamGroup').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteCamGroup').click(function () {
    var camID = $('#ModalDeleteCamGroup').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/demo_group/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });


  $.ajax({
    type: 'GET',
    url: database_url + "/demo_group/get",
    success: function (data) {
      console.log(data)
      JSON.parse(data).forEach((results, index) => {
        
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateCamGroup' id='buttonModalActivateCamGroup' title='Click for Activate'>Inactivated</a></td>"
        if (results.demo_group_activate == "true") {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalActivateCamGroup' id='buttonModalActivateCamGroup' title='Click for Inactivate' >Activated</a></td>"
        }


        $("#showContact").append("<tr><td>" + results.name + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalUpdateCamGroup' id='buttonModalUpdateCamGroup'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteCamGroup' id='buttonModalDeleteCamGroup'>Delete</a></td><td>" +
          str_activate+"</tr>")
      })
    }
  })

});
