$(document).ready(function () {


    $(window).scroll(function () {
      let value = $(window).scrollTop();
      $('#cloud').css('left', value * 0.3 + 'px');
      $('#sun').css('top', value * 0.8 + 'px');
      $('#mount').css('top', value * 0.2 + 'px');
      if (value > 500) {
        $('#sun').css('display', 'none');
      } else {
         $('#sun').css('display', 'block');
         }

      if (value > 50) {
        if ($(".back-top").hasClass("hide")) {
          $(".back-top").toggleClass("hide");
        }
      } else {
        $(".back-top").addClass("hide");
      }
    });
  

    $(".back-top").on("click", function (event) {
      $("html, body").animate(
        {
          scrollTop: 0
        },
        10 
      );
    });
  });