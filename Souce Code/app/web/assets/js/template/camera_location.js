var database_endpoint = database_url + '/camera_stream/get'

fetch(database_endpoint)
  .then(response => response.json())
  .then(json => 
  
    json.forEach(function (item, index) {
        console.log(item, index);

        var cameraName = item['name'];
        var CameraID = item['_id'].$oid;
        // var cameraServer = item['server']
        var cameraLat = item['latitude'];
        var cameraLng = item['longitude'];

        console.log(CameraID);
        console.log("************");
        
        // http://172.21.10.14/mjpg/video.mjpg?camera=1
        // L.marker([cameraLat, cameraLng], {icon: cameraIcon}).addTo(map).bindPopup("<b>"+cameraName+"</b><br><img src='http://"+cameraServer+"/stream/" + CameraID + "' height='300px' width='400px'>",{'autoClose': true, 'closeOnClick':false, maxWidth : 480}).openPopup();
        L.marker([cameraLat, cameraLng], {icon: cameraIcon}).addTo(map).bindPopup("<b>"+cameraName+"</b><br><img src='http://172.21.10.14/mjpg/video.mjpg?camera=1' height='300px' width='400px'>",{'autoClose': true, 'closeOnClick':false, maxWidth : 480}).openPopup();

    })
  
  );