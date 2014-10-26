$(document).ready(function() {
  $('form#login-form').submit(function(e) {
    e.preventDefault();
    var username = $("#login-form input#dtu-id").val();
    var password = $("#login-form input#password").val();

    console.log(e);
    console.log(e.action);
    $.ajax({
      type: "GET",
      url: "/auth",
      contentType: 'application/json',
      async: false,
      username: username,
      password: password,
      beforeSend: function (xhr) {
        xhr.setRequestHeader(
          "Authorization",
          "Basic " + btoa(username + ":" + password)
        );
      },
      error: function(xhr, textStatus, errorThrown) {
        alert('error')
      },
      success: function (data, textStatus, xhr){
        window.location.href = '/cv';
      }
    });

    return false;
  });
});
