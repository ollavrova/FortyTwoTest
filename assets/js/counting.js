 /*<![CDATA[*/
$(document).ready(function() {
    var counter = false;
    var old_time;
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    // setup ajax post, add csrftoken
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(window).focus(function() {
        console.log("focus came");
        if (counter) {
            clearInterval(counter);};
          // refresh all info about count if focus came
            $('#result_upload').val(0);
            $('#result').val(0);
            $('title').text('Requests list');
        }).blur(function() {
            console.log("blur came");
            old_time = new Date().toJSON().replace('T', ' ').slice(0,-1);
        counter = setInterval("ask()", 3000);
});
});

 function ask() {
    $.ajax({
            type: "POST",
            url: "/requests/",
            data: { old_time: $("#request_old_time").val().trim(),
            'csrfmiddlewaretoken': $('#csrfmiddlewaretoken').val(),
                },
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                // check old count of new requests if exists
                reset1 = parseInt($('#result').val(), 10);
                console.log('old result = ' + reset1);
                // write new count
                $('#result_upload').val(data.result);
                reset2 = parseInt($('#result_upload').val(), 10);
                // add old and new number
                if (!reset1) {
                    res = reset2;
                } else {
                    res = reset1 + reset2;
                };
                console.log('new requests - '+ reset2);
                console.log('result = ' + res);
                // add number in title
                if (res) {
                    $('title').text('('+ res +') Requests list');
                    // update time of calculation
                    $("#request_old_time").val(data.old_time);
                    // update result count
                    $("#result").val(res);
                };
            },
            error: function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log('ajax error!');
                console.log( "Request Failed: " + err );
            }
        });
};

/*]]>*/
