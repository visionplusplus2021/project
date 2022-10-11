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


var cameraIcon = L.icon({
  iconUrl: 'camera.png',
  iconSize: [30, 30]
});