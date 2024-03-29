$(document).ready(function(){
    $('.sidenav').sidenav(); //Sidenav
    $('.pushpin').pushpin({ //Table of content on the post-detail
    top: 100,
    offset: 170
    });
    $('img').addClass('responsive-img'); // This enables image's responsiveness
    $('img').addClass('materialboxed'); // This enables image's close up
    $('.post-body ul').addClass('browser-default'); // Restore bullets on <ul> since Materialize removes it by its default
    $('.admonition').addClass('z-depth-2'); // Adds Materialize shadow to admonition div

    $('.dropdown-trigger').dropdown({
    coverTrigger: false
    // specify options here
    });
    var dd = $('#auth').dropdown({
    constrainWidth: false,
    coverTrigger: false,
    closeOnClick: false,
    autoTrigger: false,
    alignment: 'left',
    });

    $('#log_in_discussion').click(function(){
    $('html,body').animate({ scrollTop: 0 }, 'slow');
    var dropdownInstance = M.Dropdown.getInstance(dd);
    dropdownInstance.open();
    return false;
    });

    $('#sign_in_form').submit(function(e){
        e.preventDefault();
        var urlLocation = $(location).attr("href");
        $.ajax({
            url: '{% url "login" %}',
            type: "POST",
            dataType: 'json',
            data: {
                username: $('#id_username').val(),
                password: $('#id_password').val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                if (data.valid) {
                    window.location.href = urlLocation;
                }
                else {
                    var dropdownInstance = M.Dropdown.getInstance(dd);
                    $('#errors').empty()
                    var json_str = JSON.stringify(data);
                    var json_data = JSON.parse(json_str);
                    var errors = JSON.parse(json_data.errors);
                    $.each(errors, function(index, value) {
                        $.each(value, function(index, value2) {
                            $('#errors').append(value2.message);
                        });
                    });
                    $('#errors').show()
                    dropdownInstance.recalculateDimensions();
                };
            },
            error: function(data){
                console.log(data);
                console.log('error');
            }

        });
    });
    $('#sign_in_form').on('keydown', function(event) {
        event.stopPropagation();
    });
});
