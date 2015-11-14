/*<![CDATA[*/
$(document).ready(function (e) {
    var options = {
        //timeout: 3000,
        datatype: 'json',
        target: $("#send-form"),   // target element(s) to be updated with server response
        beforeSubmit: beforeRequest,  // pre-submit callback
        success: function(data){ processJson(data);},  // post-submit callback
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
    var queryString = $.param(formData);
    var file = $('#id_photo').get(0).files[0];
    $("#result").html('');
    $("input").attr('disabled', true);
    $("textarea").attr('disabled', true);
    $("#sendbutton").attr('disabled', true);
    $("#result").prepend('<span>Saving, please wait... </span>');
    return true;
}

 function processJson(data) { console.log('process json!');
     if (data) {
         $('.errors').remove();
         if (eval(data.err)) {
             errors = eval(data.errors);
             $.each(errors, function(fieldname,errmsg)
             {
                 id = "#id_" + fieldname;
                 iderr =  "id_" + fieldname + '_errror';
                 console.log(iderr)

                 if ($('#' + iderr).length == 0){
                     $(id).parent().after($("<div class='errors' id='"+iderr+"'></div>"));
                 }
                 $('#'+iderr).html(errmsg);
                 console.log(errmsg)
             })
             $("#send-form textarea, input").attr('disabled','')

         } else {
             //$("#send-form").clearForm();
            $('#send-form').populate(data.data);
             //alert('operation is successed')
            $("input").attr('disabled', false);
            $("textarea").attr('disabled', false);
            $("#sendbutton").prop('disabled', false);
            //var errors = $('div#errors').text().trim();
            //console.log(data.errors);
            //if (errors == false) {
            //    console.log('no errors!');
                $("#result").prepend('<span>Changes have been saved.</span>');
            //};
         }
     } else {
         console.log("Ajax error : no data received.");
     }
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