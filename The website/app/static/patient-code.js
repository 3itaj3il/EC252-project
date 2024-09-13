(function(){

 // Variables
 var $curve = document.getElementById("curve");
 var last_known_scroll_position = 0;
 var defaultCurveValue = 350;
 var curveRate = 3;
 var ticking = false;
 var curveValue;

 // Handle the functionality
 function scrollEvent(scrollPos) {
   if (scrollPos >= 0 && scrollPos < defaultCurveValue) {
     curveValue = defaultCurveValue - parseFloat(scrollPos / curveRate);
     $curve.setAttribute(
       "d",
       "M 800 300 Q 400 " + curveValue + " 0 300 L 0 0 L 800 0 L 800 300 Z"
     );
   }
 }

 // Scroll Listener
 // https://developer.mozilla.org/en-US/docs/Web/Events/scroll
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


$("#search-icon").click(function() {
    $(".nav").toggleClass("search");
    $(".nav").toggleClass("no-search");
    $(".search-input").toggleClass("search-active");
  });
  
$('.menu-toggle').click(function(){
     $(".nav").toggleClass("mobile-nav");
     $(this).toggleClass("is-active");
  });

    })();

    // $(".clinic-div").click(function(){
    //     $.get('/profile', function(response){
    //         // You can handle the response here, for example:
    //         window.location.href = '/profile/{{}}'; // Redirect to the profile page
    //     });
    // });

    $('.option').click(function(){

      var selected = $('input[name="Day"]:checked').val();
      
      if (selected) {
        $(".s").prop("disabled", false);
     } else {
        $(".s").prop("disabled", true);
     }
    });
    