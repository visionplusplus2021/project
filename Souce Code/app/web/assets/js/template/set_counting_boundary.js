

  $(document).ready(function () {


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
      var landName = document.getElementById("lane_name").value;
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
        url: "/set_counting_video_boundary/"+id,
        success: function (data) {
          console.log("test");
        }
      });

    });



  });




