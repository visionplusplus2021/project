$(document).ready(function () {

  $('#buttonGroupAdd').click(function () {

    var $status = $("#statusAdd");
    var groupName = $("#inputGroupName").val();
    var groupType = $("#inputGroupType").val();

    if (groupName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Group Name.').removeClass("invisible");
    }
    else {
      // save group information in database
      const data = {
        'group_name': groupName.toLowerCase().trim(),
        'group_type': groupType,
        'user_id':user_id
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/camera_group/store",
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
    var groupType = $("#updateGroupType").val();
    if (groupName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Group Name.').removeClass("invisible");
    }
    else {
      // save group information in database
      const data = {
        'object_id': updateOID,
        'group_name': groupName.toLowerCase().trim(),
        'group_type':groupType,
        'user_id':user_id
      };

      $.ajax({
        type: 'PUT',
        url: database_url + "/camera_group/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          console.log(data.status );
          if( data.status == 422 ){
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
      url: database_url + "/camera_group/getByID/"+objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {
          
            console.log(element.server);
            $('#updateGroupName').val(element[1]);
            $('#updateGroupType').val(element[2]);

          
        })
      }
    });

  });

  $('#buttonCamGroupActivate').click(function () {
    var updateOID = $('#ModalActivateCamGroup').data('oid');

    console.log("my id: "+updateOID);

    $.ajax({
      type: 'POST',
      url: database_url + "/camera_group/activate/" + updateOID+"_"+user_id,
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
      url: database_url + "/camera_group/delete/" + camID,
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
    url: database_url + "/camera_group/get",
    success: function (data) {
      
      JSON.parse(data).forEach((results, index) => {
        console.log(results[3] )
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateCamGroup' id='buttonModalActivateCamGroup' title='Click for Activation'>Activate</a></td>"
        if (results[3] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0]  + "' data-toggle='modal' data-target='#ModalActivateCamGroup' id='buttonModalActivateCamGroup' title='Click for Inactivation' >Inactivate</a></td>"
        }

        str_group_type = "Demo Video";
        if(results[2] == 0)
        {
          str_group_type = "Live Camera";
        }
        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          str_group_type + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateCamGroup' id='buttonModalUpdateCamGroup'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteCamGroup' id='buttonModalDeleteCamGroup'>Delete</a></td><td>" +
          str_activate+"</tr>")
      })
    }
  })

});
