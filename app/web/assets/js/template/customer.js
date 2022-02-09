//Select Contact
$(document).ready(function () {
  $.ajax({
    type: 'GET',
    url: database_url + "/customer/get",
    success: function (data) {
      console.log(data)
      JSON.parse(data).forEach((results, index) => {

        var str_activate = "<td> <a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateContact' id='buttonModalActivateContact' title='Click for Activate'>Inactivated</a></td>"
        if (results[4] == true) {
          str_activate = "<td> <a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateContact' id='buttonModalActivateContact' title='Click for Inactivate'>Activated</a></td>"
        }


        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          results[3] + "</td><td>" +
          results[2] + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateCustomer' id='buttonModalUpdateCustomer'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteCustomer' id='buttonModalDeleteCustomer'>Delete</a></td>" +

          str_activate + "</tr>")
      })
    }
  })

  $('#buttonModalAddCustomer').click(function () {
    $("#showAddFeature").empty();
    $.ajax({
      type: 'GET',
      url: database_url + "/customer/get_feature",
      success: function (data) {
        console.log("========>")
        JSON.parse(data).forEach((results, index) => {
          $("#showAddFeature").append("<tr><td>" + results[1] + "</td><td>" +
            "<input type='checkbox' id='addemail" + results[0] + "' value=" + results[1] + "></input></td><td>" +
            "<input type='checkbox' id='addsms" + results[0] + "' value=" + results[1] + "></input></td>" +
            "</tr>")
        })
      }
    })
  });

  $('#btnAddContact').click(function () {

    var $status = $("#statusAdd");

    var contactName = $("#username").val();
    var email = $("#contact_email").val();
    var mobile = $("#contact_mobile").val();

    if (contactName == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Contact Name.').removeClass("invisible");
    }
    else if (email == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter Email.').removeClass("invisible");
    }
    else if (mobile == '') {
      $status.css({ "color": "red" });
      $status.text('Please Enter mobile.').removeClass("invisible");
    }
    else {

      $.ajax({
        type: 'GET',
        url: database_url + "/feature/get",
        success: function (list) {
          var temp = [];
          var features_email = [];
          var features_sms = [];
          JSON.parse(list).forEach(element => {
            if ($('input#addemail' + element[0] ).prop('checked') == true) {
              var feature = element[0]
              features_email.push(feature);
            }
            if ($('input#addsms' + element[0]).prop('checked') == true) {
              var feature = element[0]
              features_sms.push(feature);
            }


          })


          const data = {
            'contact_name': contactName,
            'email': email,
            'mobile': mobile,
            'features_email': features_email,
            'features_sms': features_sms,
            'user_id':user_id
          };
          console.log(data);
          fetch(database_url + '/customer/store', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
            .then(response => {
              if (response.status == 44) {
                $status.css({ "color": "red" });
                $status.text('"Contact Name" already exists.').removeClass("invisible");
              }
              else {
                location.reload();
              }
            })
            .then(data => {
              
            })
            .catch((error) => {
              console.log(error);
            });


        }
      });
    }

  });



  $('#btnUpdateCustomer').click(function () {
    var updateOID = $('#ModalUpdateCustomer').data('oid');
    var name = $("#updateName").val();
    var email = $("#updateEmail").val();
    var mobile = $("#updateMobile").val();
    var features_email = [];
    var features_sms = [];

    $.ajax({
      type: 'GET',
      url: database_url + "/feature/get",
      success: function (list) {
        var temp = [];
        var features_email = [];
        var features_sms = [];
        JSON.parse(list).forEach(element => {
          if ($('input#email' + element[0]).prop('checked') == true) {
            var feature = element[0]
            features_email.push(feature);
          }
          if ($('input#sms' + element[0]).prop('checked') == true) {
            var feature = element[0]
            features_sms.push(feature);
          }


        })


        const data = {
          'object_id': updateOID,
          'contact_name': name,
          'email': email,
          'mobile': mobile,
          'features_email': features_email,
          'features_sms': features_sms,
          'user_id':user_id
        };
        console.log(data);
        fetch(database_url + '/customer/update', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
          .then(response => {
            if (response.status == 422) {
              alert("Contact already exists")
            }
            location.reload();
          })
          .then(data => {
          })
          .catch((error) => {
            console.log(error);
          });


      }
    });







  });

  $('#ModalUpdateCustomer').on('show.bs.modal', function (e) {
    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));


    var features_email = [];
    var features_sms = [];

    $.ajax({
      type: 'GET',
      url: database_url + "/customer/getByID/"+objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {
          
            $('#updateName').val(element[1]);
            $('#updateEmail').val(element[3]);
            $('#updateMobile').val(element[2]);

            features_email = element.features_email
            features_sms = element.features_sms


            $("#showFeature").empty();


            $.ajax({
              type: 'GET',
              url: database_url + "/customer/get_feature",
              success: function (data) {



                
                JSON.parse(data).forEach((results, index) => {
                  
                  console.log(results[4])
                  str_check_email = "unchecked";
                  str_check_sms = "unchecked";
                  if (results[4] == true) {
                    str_check_email = "checked";
                  }

                  if (results[5] == true) {
                    str_check_sms = "checked";
                  }


                  $("#showFeature").append("<tr><td>" + results[1] + "</td><td>" +
                    "<input type='checkbox' id='email" + results[0]+ "' value=" + results[1] + " " + str_check_email + "></input></td><td>" +
                    "<input type='checkbox' id='sms" + results[0] + "' value=" + results[1] + " " + str_check_sms + "></input></td>" +
                    "</tr>")
                })
              }

            })

          }
        )
      }
    });


  });

});


$('#buttonContactActivate').click(function () {
  var updateOID = $('#ModalActivateContact').data('oid');


  $.ajax({
    type: 'POST',
    url: database_url + "/contact/activate/" + updateOID,
    success: function (data) {
      location.reload();
    }
  });
});


$('#ModalActivateContact').on('show.bs.modal', function (e) {
  $(this).data("oid", $(e.relatedTarget).attr('data-id'));
});


$('#ModalActivateEmail').on('show.bs.modal', function (e) {
  $(this).data("oid", $(e.relatedTarget).attr('data-id'));
});



$('#ModalDeleteCustomer').on('show.bs.modal', function (e) {
  $(this).data("oid", $(e.relatedTarget).attr('data-id'));
});

$('#buttonDeleteCustomer').click(function () {
  var camID = $('#ModalDeleteCustomer').data('oid');

  $.ajax({
    type: 'DELETE',
    url: database_url + "/customer/delete/" + camID,
    success: function (data) {
      location.reload();
    }
  });
});