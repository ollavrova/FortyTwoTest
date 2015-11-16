/*<![CDATA[*/
$(document).ready(function (e) {
    var options = {
        //timeout: 3000,
        datatype: 'json',
        target: $("#send-form"),   // target element(s) to be updated with server response
        beforeSubmit: beforeRequest,  // pre-submit callback
        success: afterRequest,  // post-submit callback
        error: function (jqxhr, textStatus, error) {
            var err = error;
            $("#result").attr('class', 'alert-error');
            $("#result").html(err + '');
            console.log(err + ', '+ textStatus);

        }
    };
    $('#send-form').submit(function () {
        $(this).ajaxSubmit(options);
        return false;
    });
});



function beforeRequest(formData, jqForm, options) {
    $("#result").html('');
    $("input").attr('disabled', true);
    $("textarea").attr('disabled', true);
    $("#sendbutton").attr('disabled', true);
    $("#result").prepend('<span>Saving, please wait... </span>');
    return true;
}

function afterRequest(responseText, statusText, xhr, $form) {
    console.log("success");
    $("input").attr('disabled', false);
    $("textarea").attr('disabled', false);
    $("#sendbutton").prop('disabled', false);
    var errors = $('div#errors').text().trim();
    console.log(errors);
    if (errors == false) {
        console.log('no errors!');
        $("#result").prepend('<span>Changes have been saved.</span>');
    };
};

// preview of photo
window.onload = function(){
  function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#image_edit').attr('src', e.target.result);
                $('#image_edit').attr('style', 'display: block');
            }

            reader.readAsDataURL(input.files[0]);
        } else {$('#image_edit').attr('style', 'display: None'); };
    }

    $("#id_photo").change(function(){
        readURL(this);
    });
};
/*]]>*/