$.get(
  "https://ipinfo.io",
  function(response) {
    $("#ip").html("IP: <b>" + response.ip + "</b>");
    $("#country").html("Country: <b>" + response.country + "</b>");
    $("#city").html(
      "City: <b>" + response.city + ", " + response.state + "</b>"
    );
    $("#state").html("State: <b>" + response.ip + "</b>");
  },
  "jsonp"
);
