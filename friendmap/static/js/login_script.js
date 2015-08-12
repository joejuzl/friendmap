
function login() {
    var username = $("#inputUsername").val();
    var password = $("#inputPassword").val();
    var data = {
        "username": username,
        "password": password
    };
    $.ajax({
        type: "POST",
        url: "/login_user/",
        contentType: 'application/json',
        data: JSON.stringify(data),
        complete: function(jqXHR) {
            switch (jqXHR.status){
                case 200:
                    $.cookie('loggedin', jqXHR.responseText);
                    window.location.replace("/");
                    break;
                default :
                    $(".error-signal").addClass('has-error')
            }
        }

    });
}
function signup() {
    var username = $("#inputUsername").val();
    var password = $("#inputPassword").val();
    var data = {
        "username": username,
        "password": password
    };
    $.ajax({
        type: "POST",
        url: "/users/",
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (response) {
            login();
        }
    });
}

function logout() {
    $.ajax({
        type: "POST",
        url: "/logout_user/",
        success: function (response) {
            $.removeCookie('loggedin');
            window.location.replace("/login_form");
        }
    });
}
