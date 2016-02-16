/**
 * Created by dfitzgerald on 2/16/16.
 */
$(document).ready(function(){
    $('#register_submit').click(function(){
        if($('#id_password').val() != $('#password_confirm').val()){
            $('#passwords_do_not_match').css('display', 'inline');
            window.setTimeout(function(){
                $('#passwords_do_not_match').fadeOut(500);
            }, 4000);
        }else{
            console.log('Same pasword!');
            $('form').submit();
        }
    });
});
