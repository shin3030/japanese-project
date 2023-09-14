
$(document).ready(function () {


    $(window).scroll(function () {
      let value = $(window).scrollTop();
      $('#cloud').css('left', value * 0.3 + 'px');
      $('#cloud').css('top', value * 0.15 + 'px');
      $('#sunrisecloud').css('left', value * 0.3 + 'px');
      $('#sunrisecloud').css('top', value * 0.3 + 'px');
      $('#sunsetcloud').css('left', value * 0.2 + 'px');
      $('#sunsetcloud').css('top', value * 0.25 + 'px');
      $('#sun').css('top', value * 0.4 + 'px');
      $('#sun').css('left', value * 0.4 + 'px');
      $('#sunset').css('top', value * 0.4 + 'px');
      $('#mount').css('top', value * 0.3 + 'px');
      if (value > 500) {
        $('#sun').css('display', 'none');
      } else {
         $('#sun').css('display', 'block');
         }

      if (value > 200) {
        if ($(".back-top").hasClass("hide")) {
          $(".back-top").toggleClass("hide");
        }
      } else {
        $(".back-top").addClass("hide");
      }
      if (value > 1400) {
        if ($(".yuko").hasClass("hideimg")) {
          $(".yuko").toggleClass("hideimg");
        }
      } else {
        $(".yuko").addClass("hideimg");
      }

    });
  

    $(".back-top").on("click", function (event) {
      $("html, body").animate(
        {
          scrollTop: 0
        },
        50
      );
    });

    AOS.init();
    
  });
  
    
