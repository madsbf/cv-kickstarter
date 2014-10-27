$(document).ready(function() {
  loginViewModel = {
    submitButtonElement: $("form#login-form button[type='submit']"),
    errorMessageElement: $("#login-form-error"),

    onSubmission: function() {
      this._disableLoginButton();
      this._showSpinner();
    },
    onSubmissionComplete: function() {
      this._enableLoginButton();
      this._hideSpinner();
    },
    showErrorMessage: function(errorMessage) {
      this.errorMessageElement.removeClass('hidden').html(errorMessage)
    },
    hideErrorMessage: function() {
      this.errorMessageElement.addClass('hidden').html('')
    },
    goToPage: function(url) {
      window.location.href = url;
    },
    _showSpinner: function() {
      this.submitButtonElement.addClass('login-form-spinner');
    },
    _hideSpinner: function() {
      this.submitButtonElement.removeClass('login-form-spinner');
    },
    _disableLoginButton: function() {
      this.submitButtonElement.attr('disabled', true);
    },
    _enableLoginButton: function() {
      this.submitButtonElement.attr('disabled', false);
    },
  };

  $('form#login-form').submit(function(e) {
    e.preventDefault();
    var username = $("#login-form input#dtu-id").val();
    var password = $("#login-form input#password").val();

    $.ajax({
      type: "GET",
      url: "/auth",
      contentType: 'application/json',
      username: username,
      password: password,
      beforeSend: function (xhr) {
        loginViewModel.onSubmission();
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
        loginViewModel.onSubmissionComplete();
      }
    });

    return false;
  });
});
