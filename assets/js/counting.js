 /*<![CDATA[*/
$(document).ready(function() {
    var counter = false;

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
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
        counter = setInterval("ask()", 3000);
});
});

 function ask() {
    $.ajax({
            type: "POST",
            url: "/requests/",
            data: JSON.stringify({
                old_time: $("#get_time").val(),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                // check old count of new requests if exists
                reset = parseInt($('#result').val(), 10);
                // write new count
                $('#result_upload').val(data.result);
                result_upload = parseInt($('#result_upload').val(), 10);
                // add old and new number
                if (result_upload) {
                    if (!reset) {
                        res = result_upload;
                    } else {
                        res = reset + result_upload;
                    }
                    ;
                    console.log(data.old_time + ' new requests - ' + result_upload + ', result = ' + res);
                    // add number in title
                    if (res) {
                        $('title').text('(' + res + ') Requests list');
                        // update result count
                        $("#result").val(res);
                        // update time of calculation
                        $("#get_time").val(data.old_time);
                    }
                    ;
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
