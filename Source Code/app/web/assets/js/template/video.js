
  
$(document).ready(function () {

  getServers();

  $('#buttonUploadVideo').click(function () {
      var videoName = $("#inputVideoName").val();
      var videoFile = document.getElementById('inputUploadVideoFile');
      var videoServer = $("#inputVideoServer option:selected").text();
      var $status = $("#status");

      var videoExtension = videoFile.files[0].name.split('.')[1];
      

      
      uuid = generateUUID();
     
      var data = new FormData();
      data.append('videoName', videoName);
      data.append('videoFile', videoFile.files[0]);
      data.append('videoServer', videoServer);
      data.append('uuid', uuid);

      // // saving video file to the remote server
      // $.ajax({
      //   type:'POST',
      //   url: 'http://199.212.33.166:9905/uploader',
      //   data: data,
      //   cache:false,
      //   contentType: false,
      //   processData: false,
      //   success:function(data){
      //     //function here
      //     // console.log('Success:', data);
      //     alert('Video is uploaded successfully')
      //   },
      //   error: function(data){
      //     //function here
      //     // console.log('Error:', data)
      //     alert('Failed:', data)
      //   }
      // });


      //########## Upload File
      var request = new XMLHttpRequest();
      var params = "UID=CORS&name=CORS";
      request.timeout = 60000;

      request.onreadystatechange = function () {


        
        //Connect to the server sucessfully

        console.log(" readyState= "+request.readyState+ " , status= "+request.status);
        
        $status.css({ "color": "orange" });
        $status.text("Uploading file... ").removeClass("invisible");
      
        
        if (request.readyState === 4) {
          if (request.status === 200) {

            $status.css({ "color": "green" });
            $status.text("Uploading file completed... ").removeClass("invisible");

            const data_insert = {
              'video_name': videoName,
              'uuid': uuid,
              'user_id': user_id

            };
      
            // storing video informatino in the database
            $.ajax({
              type: 'POST',
              url: database_url + "/video/store",
              data: data_insert,
              dataType: "text",
              success: function (data) {
                console.log(data);
                location.reload();
              },
              error: function (data) {
                console.log(data);
              }
            });

            
          }
        }else
        {
          console.log("waiting !!! ");
        }
      };
     
      request.open('POST', "http://199.212.33.166:6101/uploader", true);
      request.send(data);



      
      
    });

    function generateUUID() { // Public Domain/MIT
      var d = new Date().getTime();//Timestamp
      var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = Math.random() * 16;//random number between 0 and 16
          if(d > 0){//Use timestamp until depleted
              r = (d + r)%16 | 0;
              d = Math.floor(d/16);
          } else {//Use microseconds since page-load if supported
              r = (d2 + r)%16 | 0;
              d2 = Math.floor(d2/16);
          }
          return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
      });
  }

    function getServers() {
      $.ajax({
        type: 'GET',
        url: database_url + "/server/get_activate",
        success: function (data) {
          // var temp1 = ["<option value='0'>Unlisted</div>"];
          var temp1 = [];
          JSON.parse(data).forEach(function (element, index) {
            temp1.push("</div><option value=" + element._id.$oid + ">" + element.server_ip + ":" + element.server_port + "</option></div>");
          });
          $('#inputVideoServer').html(temp1);
          $('#updateVideoServer').html(temp1);
          // $('#inputCameraServer').val("0");
        }
      });
    }


    $('#ModalDeleteVideo').on('show.bs.modal', function (e) {
      $(this).data("oid", $(e.relatedTarget).attr('data-id'));
      $(this).data("name", $(e.relatedTarget).attr('data-name'));
      $(this).data("server", $(e.relatedTarget).attr('data-server'));
    });
  
    $('#buttonDeleteVideo').click(function () {
      var id = $('#ModalDeleteVideo').data('oid');
      var name = $('#ModalDeleteVideo').data('name');
      var server = $('#ModalDeleteVideo').data('server');
      
      console.log('id '+id);
      console.log('name '+name);
      console.log('server '+server);

      // // deleting video file from server
      // $.ajax({
      //   type: 'DELETE',
      //   url: 'http://'+ server + "/video_demo_file/delete/" + name,
      //   success: function (data) {
      //     location.reload();
      //   }
      // });

      // deleting from database
      $.ajax({
        type: 'DELETE',
        url: database_url + "/video_demo_file/delete/" + id,
        success: function (data) {
          location.reload();
        }
      });
    });



  $.ajax({
    type: 'GET',
    url: database_url + "/video_demo_file/get",
    success: function (data) {
      JSON.parse(data).forEach((results, index) => {

        $("#showContact").append("<tr><td>" + results[1] + "</td><td>" +
          "<a class='btn btn-danger btn-sm' data-title='Delete' data-server='" + results[0] + "' data-name='" + results[0] + "' data-id='" + results[0] + "' data-toggle='modal' data-target='#ModalDeleteVideo' id='buttonModalDeleteVideo'>Delete</a></td>" +
          "</tr>")
      })
    }
  })

});

