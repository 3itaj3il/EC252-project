$(function(){

    $('.button-success').click(function(){
        localStorage.type = $(this).val();
        if(localStorage.type == 'clinic'){
            $('.log-form form').attr('action', '/clinic');
        }else if(localStorage.type == 'patient'){
            $('.log-form form').attr('action', '/home');
        }
        
        $('.first-one').prop('hidden', true);
        $('.log-form').prop('hidden', false);
      })

    if(localStorage.type) {
        $('.type').val(localStorage.type) 
    }
    var $checkbox = $('#stacked-remember');
    var $email = $('#stacked-email');

    if(localStorage.checkbox && localStorage.checkbox !== ""){
        $email.val(localStorage.user);
        $checkbox.prop('checked', true);
        $('.first-one').prop('hidden', true);
        $('.log-form').prop('hidden', false);
    }else{
        $checkbox.prop('checked', false);
        $email.val('');
    };

    $('.log-form').submit(function(){
        if ($checkbox.is(':checked') && $email.val() !== "") {
          localStorage.user = $email.val();
          localStorage.checkbox = $checkbox.val();
        } else {
          localStorage.user = "";
          localStorage.checkbox = "";
          localStorage.type = "";
        }
      })

      $('.log-form span').click(function(){
            if(localStorage.type == 'clinic'){
                $('.clinic-form').prop("hidden", false)
            }else{
                $('.patient-form').prop("hidden", false)
            }
            $('.log-form').prop("hidden", true)
      })

      $('.clinic-form span, .patient-form span').click(function(){
        if(localStorage.type == 'clinic'){
            $('.clinic-form').prop("hidden", true)
        }else{
            $('.patient-form').prop("hidden", true)
        }
        $('.log-form').prop("hidden", false)
  })

  $('.clinic-form input').blur(function(){
    f = 1
    $('.clinic-form input').each(function(){
        if ($(this).val() === '') {
            console.log($(this).val())
            f = 0;
            return;
        }
    });});

      $('.clinic-form input').keyup(function(){
        f = 1
        $('.clinic-form input').each(function(){
            if ($(this).val() === '') {
                console.log($(this).val())
                f = 0;
                return;
            }
        });

        var regex = /^[A-Za-z]+$/;
        var name = regex.test($('.clinic-form .name').val());
        var emailValid = $('.clinic-form .signin-email').val().search('@') !== -1;
        var phoneValid = $('.clinic-form .phone').val().trim().search(/^(091|092|093|094)\d{7}$/) !== -1;
        var locationValid = $('.clinic-form .location').val().trim().search(/^https?:\/\/(www\.)?google\.[a-z]+\/maps(\/.*)?$/) !== -1;
        var passLen = $(".clinic-form .pass").val().length >= 8
        var matchingPass = $(".clinic-form .pass").val() == $(".clinic-form .pass2").val();

        if (f && emailValid && phoneValid && locationValid && matchingPass && passLen && name) {
            $(".clinic-form .s").prop("disabled", false);
        } else {
            $(".clinic-form .s").prop("disabled", true);
        }

        if($(this).val() == ''){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");
            
        }else{
            $(this).css("border-color", '#999')
            $(this).prev().css("color", "#eaf6f6");
        }

        if($(this).hasClass('signin-email') && !emailValid){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");    
        }

        if($(this).hasClass('phone') && !phoneValid){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");
            
        }
        
        if($(this).hasClass('location') && !locationValid){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");
            
        }

        if(!matchingPass){
            $('.clinic-form .pass2').css("border-color", 'red');
            $('.clinic-form .pass2').prev().css("color", "red");
            
        }

        if($(this).hasClass('pass') && !passLen){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");
            
        }

        if($(this).hasClass('name') && !name){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");    
        }
      })

      $('.patient-form input').keyup(function(){
        f = 1
        $('.patient-form input').each(function(){
            if ($(this).val() === '') {
                console.log($(this))
                f = 0;
                return;
            }
        });

        var regex = /^[A-Za-z]+$/;
        var emailValid = $('.patient-form .signin-email').val().search('@') !== -1;
        var name = regex.test($('.patient-form .name').val());
        var phoneValid = $('.patient-form .phone').val().trim().search(/^(091|092|093|094)\d{7}$/) !== -1;
        var passLen = $(".patient-form .pass").val().length >= 8
        var matchingPass = $(".patient-form .pass").val() == $(".patient-form .pass2").val();

        if (f && emailValid && phoneValid && matchingPass && passLen && name) {
            $(".patient-form .s").prop("disabled", false);
        } else {
            $(".patient-form .s").prop("disabled", true);
        }

        if($(this).val() == ''){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");
            
        }else{
            $(this).css("border-color", '#999')
            $(this).prev().css("color", "#eaf6f6");
        }

        if($(this).hasClass('signin-email') && !emailValid){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");     
        }

        if($(this).hasClass('phone') && !phoneValid){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");    
        }

        if(!matchingPass){
            $('.patient-form .pass2').css("border-color", 'red');
            $('.patient-form .pass2').prev().css("color", "red");    
        }

        if($(this).hasClass('pass') && !passLen){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");    
        }

        if($(this).hasClass('name') && !name){
            $(this).css("border-color", 'red');
            $(this).prev().css("color", "red");    
        }
      })

    
        let alertBox = $("#alert");
            setTimeout(function() {
                alertBox.fadeOut(2000);;
            }, 1000); 
})