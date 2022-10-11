//Select Contact
$(document).ready(function () {
  
    $.ajax({
      type: 'GET',
      url: database_url + "/vehicle/get",
      success: function (data) {
        console.log(data)
        JSON.parse(data).forEach((results, index) => {
          $("#showContact").append("<tr><td>" + results.timestamp + "</td><td>" +
            results._id.$oid + "</td><td>" +
            results.server + "</td><td>" +
            results.from + "</td><td>" +
            results.to + "</td><td>" +
            results.class + "</td>" +
            "</tr>")
        })
      }
    })
  });