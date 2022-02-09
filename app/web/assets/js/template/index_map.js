var lat;
var lng;

$(document).ready(function () {

  var map = L.map('mapid').setView([43.948062, -78.895996], 16);

  var title = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidmlzaW9ucGx1c3BsdXMiLCJhIjoiY2tzdWI5OGJhMWVzNjJ1a3RpbGtzY2NnbCJ9.GhXsFiK_dl2OW05L1ND-vg', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    zoomControl: true,
    maxZoom: 25,
    minZoom: 0,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoidmlzaW9ucGx1c3BsdXMiLCJhIjoiY2tzdWI5OGJhMWVzNjJ1a3RpbGtzY2NnbCJ9.GhXsFiK_dl2OW05L1ND-vg'
  }).addTo(map);


  $('#ModalAddCamera').on('shown.bs.modal', function (e) {
    map.invalidateSize();
    console.log('reloaded leaflet');
  })

  function roadPointSwitch() {
    var p = L.popup({ offset: [0, -30], autoPan: false })
    map.on('click', onMapClick);
    map.on('mousemove', function (e) {
      p.setLatLng(e.latlng).setContent("<b>Set Camera Location:</b>" + "<br>" + "Latitude : " + e.latlng.lat + "<br>" + "Longitude : " + e.latlng.lng).openOn(map);
    });
    map.on('mouseout', function (e) {
      map.closePopup();
    });
    document.getElementById('mapid').classList.add('customCursor');
  }
  roadPointSwitch();



  var circleMarker;
  function onMapClick(e) {
    lat = e.latlng.lat;
    lng = e.latlng.lng;

    var circleMarker = new L.Marker([lat, lng], {
      draggable: true
    }).addTo(map);

    circleMarker.bindPopup("<b>Camera Location:</b>" + "<br>" + "Latitude : " + lat + "<br>" + "Longitude : " + lng, { 'autoClose': false, 'closeOnClick': false }).openPopup();

    circleMarker.on('dragend', function (e) {
      lat = circleMarker.getLatLng().lat;
      lng = circleMarker.getLatLng().lng;
      circleMarker.bindPopup("<b>Camera Location:</b>" + "<br>" + "Latitude : " + lat + "<br>" + "Longitude : " + lng, { 'autoClose': false, 'closeOnClick': false }).openPopup();

      console.log([lat, lng]);
    });

    console.log([lat, lng]);
    map.off('click');
    map.off('mousemove');
    document.getElementById('mapid').classList.remove('customCursor');

  };

});

var lat;
var lng;

$(document).ready(function () {

  var map = L.map('updateMapId').setView([43.948062, -78.895996], 16);

  var title = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidmlzaW9ucGx1c3BsdXMiLCJhIjoiY2tzdWI5OGJhMWVzNjJ1a3RpbGtzY2NnbCJ9.GhXsFiK_dl2OW05L1ND-vg', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    zoomControl: true,
    maxZoom: 25,
    minZoom: 0,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoidmlzaW9ucGx1c3BsdXMiLCJhIjoiY2tzdWI5OGJhMWVzNjJ1a3RpbGtzY2NnbCJ9.GhXsFiK_dl2OW05L1ND-vg'
  }).addTo(map);


  $('#ModalUpdateCamera').on('shown.bs.modal', function (e) {
    map.invalidateSize();
    console.log('reloaded leaflet');
  })

  function roadPointSwitch() {
    var p = L.popup({ offset: [0, -30], autoPan: false })
    map.on('click', onMapClick);
    map.on('mousemove', function (e) {
      p.setLatLng(e.latlng).setContent("<b>Set Camera Location:</b>" + "<br>" + "Latitude : " + e.latlng.lat + "<br>" + "Longitude : " + e.latlng.lng).openOn(map);
    });
    map.on('mouseout', function (e) {
      map.closePopup();
    });
    document.getElementById('updateMapId').classList.add('customCursor');
  }
  roadPointSwitch();



  var circleMarker;
  function onMapClick(e) {
    lat = e.latlng.lat;
    lng = e.latlng.lng;

    var circleMarker = new L.Marker([lat, lng], {
      draggable: true
    }).addTo(map);

    circleMarker.bindPopup("<b>Camera Location:</b>" + "<br>" + "Latitude : " + lat + "<br>" + "Longitude : " + lng, { 'autoClose': false, 'closeOnClick': false }).openPopup();

    circleMarker.on('dragend', function (e) {
      lat = circleMarker.getLatLng().lat;
      lng = circleMarker.getLatLng().lng;
      circleMarker.bindPopup("<b>Camera Location:</b>" + "<br>" + "Latitude : " + lat + "<br>" + "Longitude : " + lng, { 'autoClose': false, 'closeOnClick': false }).openPopup();

      console.log([lat, lng]);
    });

    console.log([lat, lng]);
    map.off('click');
    map.off('mousemove');
    document.getElementById('updateMapId').classList.remove('customCursor');

  };

});