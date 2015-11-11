/*<![CDATA[*/
$(document).ready(function (e) {
    var options = {
        timeout: 1000,
        datatype: 'json',
        target: $("#send-form"),   // target element(s) to be updated with server response
        beforeSubmit: beforeRequest,  // pre-submit callback
        success: afterRequest,  // post-submit callback
        error: function (jqxhr, textStatus, error) {
            var err = error;
            $("#result").attr('class', 'alert-error');
            $("#result").html(err + '! Request error! Check connection please');

        }
    };
    $('#send-form').submit(function () {
        $(this).ajaxSubmit(options);
        return false;
    });
});



function beforeRequest(formData, jqForm, options) {
    var queryString = $.param(formData);
    var file = $('#id_photo').get(0).files[0];
    $("#result").html('');
    $("#sendbutton").attr('disabled', true);
    $("#send-form").attr('disabled', true);
    $("#result").prepend('<span>Saving, please wait... </span>');
    return true;
}

function afterRequest(responseText, statusText, xhr, $form) {
    $("#sendbutton").prop('disabled', false);
    $("#send-form").prop('disabled', false);
    var errors = $('div#errors').text().trim();
    console.log(errors);
    if (errors == false) {
        console.log('no errors!');
        $("#result").prepend('<span>Changes have been saved.</span>');
    };
};

window.onload = function(){
  function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#image_edit').attr('src', e.target.result);
                $('#image_edit').attr('style', 'display: block');
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_photo").change(function(){
        readURL(this);
    });
};
/*]]>*/