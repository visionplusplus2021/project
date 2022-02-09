//Select Contact
$(document).ready(function () {

  $('#ModalDeleteLane').on('show.bs.modal', function (e) {
    $(this).data("oid", $(e.relatedTarget).attr('data-id'));
  });

  $('#buttonDeleteLane').click(function () {
    var landID = $('#ModalDeleteLane').data('oid');
    console.log("==========+> delete " + landID);
    $.ajax({
      type: 'DELETE',
      url: database_url + "/counting_boundary/delete/" + landID,
      success: function (data) {
        location.reload();
      }
    });
  });




  str_url = document.URL.split("/");
  camera_id = str_url[4];
  $.ajax({
    type: 'GET',
    url: database_url + "/counting_boundary/get/" + camera_id,
    success: function (data) {
      console.log(data)
      JSON.parse(data).forEach((results, index) => {

        console.log(results);
        $("#showCounting").append("<tr><td>" + results.lane_name + "</td><td>" +
          results.lane_type + "</td><td style='display:block;text-overflow: ellipsis;width: 300px;overflow: hidden; white-space: nowrap;'>" +
          results.start_point + "</td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-id='" + results._id.$oid + "' data-toggle='modal' data-target='#ModalDeleteLane' id='buttonModalDeleteLane'>Delete</a></td>" +

          + "</tr>")
      })
    }
  })


  $('img').click(function (e) {
    var offset_t = $(this).offset().top - $(window).scrollTop();
    var offset_l = $(this).offset().left - $(window).scrollLeft();
    w = $(this).prop("width");        // Width  (Rendered)
    h = $(this).prop("height");        // Height (Rendered)
    nw = $(this).prop("naturalWidth");  // Width  (Natural)
    nh = $(this).prop("naturalHeight"); // Height (Natural)
    var left = Math.round((e.clientX - offset_l));
    var top = Math.round((e.clientY - offset_t));
    x_data = Math.round((left * nw) / w);
    y_data = Math.round((top * nh) / h);

    var id = document.getElementById("id").value; 
    var server_name = document.getElementById("server_name").value; 
    var landName = document.getElementById("landName").value;
    var flexType = $("input:radio[name=flexType]:checked").val()



    var polygon = document.getElementById("polygon").value;
    polygon += "(" + x_data + "," + y_data + ")"
    document.getElementById('polygon').value = polygon;
    console.log("=======>" + x_data);

    const data = {
      'id':id,
      'lane_name': landName,
      'lane_type': flexType,
      'polygon':polygon,
      'x':x_data,
      'y':y_data

    };

    $.ajax({
      type: 'POST',
      data: data,
      url: "/set_counting_boundary/"+id,
      success: function (data) {
        console.log("test");
      }
    });

    var c = document.getElementById("img");
    console.log(c)
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(100, 75, 50, 0, 2 * Math.PI);
    ctx.stroke();


  });


});

