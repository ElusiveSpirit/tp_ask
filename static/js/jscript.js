/**
 * Created by konstantin on 30.03.16.
 */
 /*
(function ($) {
  $('.spinner .btn:first-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) + 1);
  });
  $('.spinner .btn:last-of-type').on('click', function() {
    $('.spinner input').val( parseInt($('.spinner input').val(), 10) - 1);
  });
})(jQuery);
*/
function likeQ(button, q_id, like) {
    // TODO Ajax request

    $.ajax({
        url:  '/like_question/',
        type: 'POST',
        data: {
            'q_id' : q_id,
            'like' : like,
            'csrfmiddlewaretoken' : getCookie('csrftoken')
        },
    }).success(function(data) {
        console.log('http ' + data.status + ' ' + data.message);
        if (data.status == 'ok') {
            button.setAttribute("disabled", "");
            if (like == 1) {
                button.nextElementSibling.removeAttribute("disabled");
            } else {
                button.previousElementSibling.removeAttribute("disabled");;
            }
            var input = button.parentNode.previousElementSibling;
            input.setAttribute("value", data.likes);
        }
    }).error(function() {
        console.log('http error');
    });
}

function likeA(a_id, like) {
    // TODO Ajax request
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
