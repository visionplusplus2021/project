//Select Contact
$(document).ready(function () {
  
    $.ajax({
      type: 'GET',
      url: database_url + "/pedestrian/get",
      success: function (data) {
        console.log(data)
        JSON.parse(data).forEach((results, index) => {
          $("#showContact").append("<tr><td>" + results.timestamp + "</td><td>" +
            results._id.$oid + "</td><td>" +
            results.name + "</td><td>" +
            results.class + "</td><td>" +
            "</tr>")
        })
      }
    })
  });