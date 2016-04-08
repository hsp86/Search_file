$(function(){
    alert("haha");

    function refresh_sl()
    {
        var $form = $(".login-block form");
        var method = $form[0].method;
        var action = $form[0].action;
        $.ajax({
            url: action,
            type: method,
            data: $form.serialize(),
            success: function(msg){
                if(msg == 1)
                {
                    alert("ok");
                }
            }
        });
    }
    
})