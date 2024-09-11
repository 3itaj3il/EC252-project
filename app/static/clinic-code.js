(function() {
    var $curve = document.getElementById("curve");
    var last_known_scroll_position = 0;
    var defaultCurveValue = 350;
    var curveRate = 3;
    var ticking = false;
    var curveValue;
  
    function scrollEvent(scrollPos) {
      if (scrollPos >= 0 && scrollPos < defaultCurveValue) {
        curveValue = defaultCurveValue - parseFloat(scrollPos / curveRate);
        $curve.setAttribute(
          "d",
          "M 800 300 Q 400 " + curveValue + " 0 300 L 0 0 L 800 0 L 800 300 Z"
        );
      }
    }
  
    window.addEventListener("scroll", function(e) {
      last_known_scroll_position = window.scrollY;
  
      if (!ticking) {
        window.requestAnimationFrame(function() {
          scrollEvent(last_known_scroll_position);
          ticking = false;
        });
      }
  
      ticking = true;
    });
  })();

  $("#search-icon").click(function() {
    $(".nav").toggleClass("search");
    $(".nav").toggleClass("no-search");
    $(".search-input").toggleClass("search-active");
  });
  
  $('.menu-toggle').click(function(){
     $(".nav").toggleClass("mobile-nav");
     $(this).toggleClass("is-active");
  });

  
  $('.doc-form input').blur(function(){
    f = 1
    $('.doc-form input').each(function(){
        if ($(this).val() === '') {
            console.log($(this))
            f = 0;
            return;
        }
    });
    
    if (f) {
        $(".doc-form .s").prop("disabled", false);
    } else {
        $(".doc-form .s").prop("disabled", true);
    }

    if($(this).val() == ''){
        $(this).css("border-color", 'red');
        $(this).prev().css("color", "red");
        
    }else{
        $(this).css("border-color", '#999')
        $(this).prev().css("color", "#eaf6f6");
    }

  })

  $('.doc-form input').keyup(function(){
    f = 1
    $('.doc-form input').each(function(){
        if ($(this).val() === '') {
            console.log($(this))
            f = 0;
            return;
        }
    });

    
    if (f) {
        $(".doc-form .s").prop("disabled", false);
    } else {
        $(".doc-form .s").prop("disabled", true);
    }

    if($(this).val() == ''){
        $(this).css("border-color", 'red');
        $(this).prev().css("color", "red");
        
    }else{
        $(this).css("border-color", '#999')
        $(this).prev().css("color", "#eaf6f6");
    }

  })

  