//Select Contact
$(document).ready(function () {

    $('#buttonCrosswalkAdd').click(function () {
    //   var routeServer = $("#inputRouteServer").val();
      var crosswalkServer = $("#inputCrosswalkServer option:selected" ).text();
      var crosswalkName = $("#inputCrosswalkName").val();
  
      console.log('Crosswalk Server: ' + crosswalkServer);
      console.log('Crosswalk Name: ' + crosswalkName);
  
      // save group information in database
      const data = {
        'crosswalkServer': crosswalkServer,
        'crosswalkName': crosswalkName
      };
  
      $.ajax({
        type: 'POST',
        url: database_url + "/crosswalk/store",
        data: data,
        dataType: "text",
        success: function (data) {
          location.reload()
        },
        error: function (data) {
          alert("Please check all fields.")
        }
      });
    });
  
    $('#buttonCrosswalkUpdate').click(function () {
      var updateOID = $('#ModalUpdateCrosswalk').data('oid');
    //   var routeServer = $("#updateRouteServer").val();
      var crosswalkServer = $("#updateCrosswalkServer option:selected" ).text();
      var crosswalkName = $("#updateCrosswalkName").val();
  
      console.log('Crosswalk server: ' + crosswalkServer);
      console.log('Crosswalk name: ' + crosswalkName);
  
    // save group information in database
    const data = {
        'object_id': updateOID,
        'crosswalkServer': crosswalkServer,
        'crosswalkName': crosswalkName
    };
  
      $.ajax({
        type: 'PUT',
        url: database_url + "/crosswalk/update",
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
  
    $('#ModalUpdateCrosswalk').on('show.bs.modal', function (e) {
      var objectID = $(e.relatedTarget).attr('data-id')
      $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  
      $.ajax({
        type: 'GET',
        url: database_url + "/crosswalk/get",
        success: function (data) {
          JSON.parse(data).forEach(element => {
            if (element._id.$oid == objectID) {
              console.log(element.server);
            //   $('#updateCrosswalkServer').val(element.server);
              $('#updateCrosswalkFrom').val(element.name);
            }
          })
        }
      });
    });
  
    $('#ModalDeleteCrosswalk').on('show.bs.modal', function (e) {
      $(this).data("oid", $(e.relatedTarget).attr('data-id'));
    });
  
    $('#buttonDeleteCrosswalk').click(function () {
      var camID = $('#ModalDeleteCrosswalk').data('oid');
  
      $.ajax({
        type: 'DELETE',
        url: database_url + "/crosswalk/delete/" + camID,
        success: function (data) {
          location.reload();
        }
      });
    });
  
    $.ajax({
      type: 'GET',
      url: database_url + "/crosswalk/get",
      success: function (data) {
        console.log(data)
        JSON.parse(data).forEach((results, index) => {
          $("#showContact").append("<tr><td>" + results.server + "</td><td>" +
            results.name + "</td><td>" +
            "<a class='btn btn-primary btn-sm' data-title='Edit' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalUpdateCrosswalk' id='buttonModalUpdateCrosswalk'>Edit</a></td><td>" +
            "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteCrosswalk' id='buttonModalDeleteCrosswalk'>Delete</a></td>" +
            "</tr>")
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
            $('#inputCrosswalkServer').html(temp1);
            $('#updateCrosswalkServer').html(temp1);
            // $('#inputCameraServer').val("0");
          }
        });
    }
    getServers();

  });