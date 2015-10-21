 /*<![CDATA[*/
$(document).ready(function() {
    var counter = false;
    var window_focus;

$(window).focus(function() {
        console.log("focus came");
        var reset, old_count;
        if (counter) {
            clearInterval(counter);};
        reset = parseInt($("#result").text(), 10);
        $('title').text('Requests list');
        $('#result_upload').text('');
        old_count= parseInt($("#request_old_count").val(), 10);
        $("#request_old_count").val(old_count+reset);
        window_focus = true;
        }).blur(function() { console.log("blur came");
            window_focus = false;
        counter = setInterval("ask()", 2000);
});
});

 function ask() {
    $.ajax({
            type: "GET",
            url: "/requests/",
            data: { request_old_count: $("#request_old_count").val()},
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                $('#result').text(data.result);
                $('title').text('('+data.result+') Requests list');
            },
            error: function (jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log('ajax error!');
                console.log( "Request Failed: " + err );
            }
        });
};
/*]]>*/
