$(document).ready(function() {
  loginViewModel = {
    submitButtonElement: $("form#login-form button[type='submit']"),
    errorMessageElement: $("#login-form-error"),

    disableLoginButton: function() {
      this.submitButtonElement.attr('disabled', true)
    },
    enableLoginButton: function() {
      this.submitButtonElement.attr('disabled', false)
    },
    showErrorMessage: function(errorMessage) {
      this.errorMessageElement.removeClass('hidden').html(errorMessage)
    },
    hideErrorMessage: function() {
      this.errorMessageElement.addClass('hidden').html('')
    },
    goToPage: function(url) {
      window.location.href = url;
    }
  };

  $('form#login-form').submit(function(e) {
    e.preventDefault();
    var username = $("#login-form input#dtu-id").val();
    var password = $("#login-form input#password").val();

    $.ajax({
      type: "GET",
      url: "/auth",
      contentType: 'application/json',
      async: false,
      username: username,
      password: password,
      beforeSend: function (xhr) {
        loginViewModel.disableLoginButton();
        xhr.setRequestHeader(
          "Authorization",
          "Basic " + btoa(username + ":" + password)
        );
      },
      error: function(xhr, textStatus, errorThrown) {
        if (xhr.status === 401) {
          loginViewModel.showErrorMessage(xhr.responseJSON.error);
        } else {
          loginViewModel.showErrorMessage("An unexpected error occured");
        }
      },
      success: function (data, textStatus, xhr){
        loginViewModel.goToPage('/cv');
      },
      complete: function(xhr, textStatus) {
        loginViewModel.enableLoginButton();
      }
    });

    return false;
  });
});
