//Select Contact
$(document).ready(function () {

  $('#buttonFeatureAdd').click(function () {
    console.log("f")

    var $status = $("#statusAdd");

    var featureName = $("#inputFeatureName").val();
    var featureEvent = $('#chkEvent').is(":checked");


    if (featureName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Feature Name.').removeClass("invisible");
    }
    else {
      console.log('Feature Name: ' + featureEvent);

      // save group information in database
      const data = {
        'feature_name': featureName.toLowerCase().trim(),
        'feature_event': featureEvent,
        'user_id':user_id
      };

      $.ajax({
        type: 'POST',
        url: database_url + "/feature/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text(" 'Feature Name' already exists").removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#buttonFeatureUpdate').click(function () {
    var $status = $("#statusUpdate");

    var updateOID = $('#ModalUpdateFeature').data('oid');
    var featureName = $("#updateFeatureName").val();
    var featureEvent = $('#chkUpdateEvent').is(":checked");
    var featureActivate = $("#updateFeatureActivate").val();

    if (featureName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Feature Name.').removeClass("invisible");
    }
    else {
      console.log(featureEvent)
      // save group information in database
      const data = {
        'object_id': updateOID,
        'feature_name': featureName.toLowerCase().trim(),
        'feature_event': featureEvent,
        'feature_activate': featureActivate,
        'user_id':user_id

      };

      $.ajax({
        type: 'PUT',
        url: database_url + "/feature/update",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          if( data.status == 422 ){
            $status.css({ "color": "red" });
            $status.text(" 'Feature Name' already exists").removeClass("invisible");
          }
          else{
          location.reload()
          }
          
        }
      });
    }
  });

  $('#buttonFeatureActivate').click(function () {
    var updateOID = $('#ModalActivateFeature').data('oid');


    $.ajax({
      type: 'POST',
      url: database_url + "/feature/activate/" + updateOID+"_"+user_id,
      success: function (data) {
        location.reload();
      }
    });
  });


  $('#ModalActivateFeature').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalUpdateFeature').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get_byID/" + objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {
          $('#updateFeatureName').val(element[1]);
          $('#updateFeatureActivate').val(element[2]);
          if (element[2] == false) {
            $('#chkUpdateEvent').prop('checked', true);
          }
          else {
            $('#chkUpdateEvent').prop('checked', false);
          }



          console.log(element.feature_name);


        });
      }
    });
  });

  $('#ModalDeleteFeature').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteFeature').click(function () {
    var camID = $('#ModalDeleteFeature').data('oid');

    $.ajax({
      type: 'DELETE',
      url: database_url + "/feature/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });

  $.ajax({
    type: 'GET',
    url: database_url + "/feature/get",
    success: function (data) {
      console.log(data)
      JSON.parse(data).forEach((results, index) => {
        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0]+ "' data-toggle='modal' data-target='#ModalActivateFeature' id='buttonModalActivateFeature' title='Click for Activatoin'>Activate</a></td>"
        if (results[3]== true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0]+ "' data-toggle='modal' data-target='#ModalActivateFeature' id='buttonModalActivateFeature' title='Click for Inactivation'>Inactivate</a></td>"
        }

        str_event = "feature </td><td>"
        if (results[2]== false) {
          str_event = "event </td><td>"
        }


        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          str_event +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateFeature' id='buttonModalUpdateFeature'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteFeature' id='buttonModalDeleteFeature'>Delete</a></td><td>" +
          str_activate
          + "</tr>")
      })
    }
  })
});

