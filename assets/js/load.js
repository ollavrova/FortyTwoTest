/*<![CDATA[*/
$(document).ready(function (e) {
    var options = {
        //timeout: 3000,
        datatype: 'json',
        target: $("#send-form"),   // target element(s) to be updated with server response
        beforeSubmit: beforeRequest,  // pre-submit callback
        success: afterRequest,  // post-submit callback
        error: function processFormError(data) { console.log('process error!');
                     if (data.responseText) {
                         $('.errors').remove();
                         $("#result").html('');
                         resp = $.parseJSON(data.responseText);
                         if (eval(resp.err)) {  console.log('process resp.err!');
                             errors = eval(resp.errs);
                             $.each(errors, function(fieldname, errmsg)
                             {   id = "#id_" + fieldname;
                                 iderr =  "id_" + fieldname + '_errror';
                                 console.log(iderr);
                                 if ($('#' + iderr).length == 0){
                                     $(id).parent().after($("<div class='errors' id='"+iderr+"'></div>"));
                                 }
                                 $('#'+iderr).html(errmsg );
                                 console.log(errmsg);
                             });
                             $("#send-form textarea, select, input").attr('disabled', false);
                             $("#result").prepend('<span>Please check error.</span>');
                         }
            else { console.log('not found errors!');
                $("#result").prepend('<span>Changes have been saved.</span>');
            };
        };
    }};
    $('#send-form').submit(function () {
        $(this).ajaxSubmit(options);
        return false;
    });
});

function beforeRequest(formData, jqForm, options) {
    var queryString = $.param(formData);
    var file = $('#id_photo').get(0).files[0];
    $("#result").html('');
    $("#send-form input textarea #sendbutton").attr('disabled', true);
    $("#result").prepend('<span>Saving, please wait... </span>');
    return true;
}

function afterRequest(responseText, statusText, xhr, $form) {
    console.log('1');
         $('.errors').remove();
    $("#send-form input textarea #sendbutton").prop('disabled', false);
    $("#result").html('');
    resp = $.parseJSON(responseText);
    console.log(' eval err: )' + (eval(resp.err)));
    $("#result").prepend('<span>Changes have been saved.</span>');
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
        }
    }

    $("#id_photo").change(function(){
        readURL(this);
    });
};
/*]]>*/