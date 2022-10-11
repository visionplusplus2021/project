//Select Contact
$(document).ready(function () {

  ///CREATE A USER
  $('#buttonCreateUser').on('click', function () {

    var name = $("#name").val();
    var email = $("#email").val();
    var password = $("#password").val();
    var userType = $('#userType :selected').val();
    var $status = $("#status");

    if (name == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter a name.').removeClass("invisible");
    } else if (email == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter an email.').removeClass("invisible");
    } else if (password == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter a password.').removeClass("invisible");
    } else {
      const data = {
        'name': name,
        'email': email,
        'password': password,
        'userType': userType,
      }

      $.ajax({
        url: location.origin + "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (data) {
          location.reload();
        },
        error: function (resp) {
          if (resp.responseText == "success") {
            location.reload();
          }
          else {

            $status.css({ "color": "red" });
            $status.text(resp.responseText).removeClass("invisible");
          }
        }
      })
    }
  });

  $('#buttonUpdateUser').click(function () {
    var updateOID = $('#ModalUpdateUser').data('oid');
    var name = $("#updateName").val();
    var email = $("#updateEmail").val();
    var password = $("#updatePassword").val();
    var userType = $("#updateUserType").val();
    var $status = $("#updstatus");

    if (name == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter a name.').removeClass("invisible");
    } else if (email == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter an email.').removeClass("invisible");
    } else if (password == '') {
      $status.css({ "color": "red" });
      $status.text('Please enter a password.').removeClass("invisible");
    } else {

      // save group information in database
      const data = {
        'object_id': updateOID,
        'name': name,
        'email': email,
        'password': password,
        'userType': userType
      };

      $.ajax({
        type: 'POST',
        url: location.origin + "/user/update",
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




  $('#buttonUserActivate').click(function () {
    var updateOID = $('#ModalActivateUser').data('oid');


    const data = {
      'object_id': updateOID
    };

    $.ajax({
      type: 'POST',
      url: location.origin + "/user/activate",
      data: data,
      dataType: "text",
      success: function (data) {
        location.reload();
      },
      error: function (data) {
        alert("Please check all fields.");
      }
    });

  });




  $('#ModalActivateUser').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#ModalUpdateUser').on('show.bs.modal', function (e) {

    var objectID = $(e.relatedTarget).attr('data-id')
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));

    $.ajax({
      type: 'GET',
      url: location.origin + "/user/get_byID/" + objectID,
      success: function (data) {
        JSON.parse(data).forEach(element => {



          $('#updateName').val(element[1]);
          $('#updateEmail').val(element[5]);
          $('#updatePassword').val(element[3]);
          $('#updateUserType').val(element[2]);



          console.log(element.name);


        });
      }
    });


  });




  $('#ModalDeleteUser').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteUser').click(function () {
    var camID = $('#ModalDeleteUser').data('oid');
    console.log(camID);

    $.ajax({
      type: 'DELETE',
      url: location.origin + "/user/delete/" + camID,
      success: function (data) {
        location.reload();
      }
    });
  });

  $.ajax({
    type: 'GET',
    url: location.origin + "/user/get",
    success: function (data) {
      console.log(data)
      JSON.parse(data).forEach((results, index) => {

        var str_activate = "<a href='#my_modal' class='btn btn-secondary btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateUser' id='buttonModalActivateUser' title='Click for Activate'>Inactivated</a></td>"
        if (results[6] == true) {
          str_activate = "<a href='#my_modal' class='btn btn-success btn-sm' data-title='Activate' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalActivateUser' id='buttonModalActivateUser' title='Click for Inactivate'>Activated</a></td>"
        }


        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          results[5] + "</td><td>" +
          results[2] + "</td><td>" +
          "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalUpdateUser' id='buttonModalUpdateUser'>Edit</a></td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteUser' id='buttonModalDeleteUser'>Delete</a></td>" +
          "<td>" + str_activate + "</tr>")
      })
    }
  })
});

