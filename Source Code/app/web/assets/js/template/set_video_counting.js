//Select Contact
$(document).ready(function () {

    $('#ModalDeleteLane').on('show.bs.modal', function (e) {
        $(this).data("oid", $(e.relatedTarget).attr('data-id'));
      });
    
      $('#buttonDeleteLane').click(function () {
        var landID = $('#ModalDeleteLane').data('oid');
        console.log("==========+> delete "+landID);
        $.ajax({
          type: 'DELETE',
          url: database_url + "/counting_video_boundary/delete/" + landID,
          success: function (data) {
            location.reload();
          }
        });
      });

    
    str_url  = document.URL.split("/");
    camera_id = str_url[4];
    $.ajax({
      type: 'GET',
      url: database_url + "/counting_video_boundary/get/"+camera_id,
      success: function (data) {
        console.log(data)
        JSON.parse(data).forEach((results, index) => {

            console.log("=====> counting video"+results);
          $("#showCounting").append("<tr><td>" + results.lane_name + "</td><td>" +
             results.lane_type + "</td><td style='display:block;text-overflow: ellipsis;width: 300px;overflow: hidden; white-space: nowrap;'>" +
             results.start_point + "</td><td>" +
            "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteLane' id='buttonModalDeleteLane'>Delete</a></td>" +

            + "</tr>")
        })
      }
    })
  });
  
  