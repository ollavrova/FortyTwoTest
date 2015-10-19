 /*<![CDATA[*/
$(document).ready(function() {
    var options = {
        target:        $("#send-form"),   // target element(s) to be updated with server response
        beforeSubmit:  beforeRequest,  // pre-submit callback
        success:       afterRequest,  // post-submit callback
        timeout: 3000
    };

    $('#send-form').submit(function() {
        $(this).ajaxSubmit(options);
        return false;
    });
});

function beforeRequest(formData, jqForm, options) {
    var queryString = $.param(formData);
    var file = $('#id_photo').get(0).files[0];
        $("#sendbutton").attr('disabled', true);
        $("#send-form").attr('disabled', true);
        $("#result").prepend('<span>Saving, please wait... </span>');
    return true;
}

function afterRequest(responseText, statusText, xhr, $form)  {
    $("#sendbutton").prop('disabled', false);
    $("#send-form").prop('disabled', false);
    $("#result").prepend('<span>Changes have been saved.</span>');
} ;
/*]]>*/