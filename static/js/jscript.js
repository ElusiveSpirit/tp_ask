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
function like(button, obj_id, like, type) {
  var url;
  if (type == 'question') {
    url = '/like_question/';
  } else {
    url = '/like_answer/';
  }
    $.ajax({
        url:  url,
        type: 'POST',
        data: {
            'obj_id' : obj_id,
            'like' : like,
            'csrfmiddlewaretoken' : getCookie('csrftoken')
        },
    }).success(function(data) {
        console.log('http ' + data.status + ' ' + data.message);
        if (data.status == 'ok') {
            if (data.vote != 0) {
               button.setAttribute("disabled", "");
            }
            if (like == 1) {
                button.nextElementSibling.removeAttribute("disabled");
            } else {
                button.previousElementSibling.removeAttribute("disabled");
            }
            var input = button.parentNode.previousElementSibling;
            input.setAttribute("value", data.likes);
        }
    }).error(function() {
        console.log('http error');
    });
}

function correctAnswer(checkbox, id, q_id) {
  checkbox.setAttribute("checked", !checkbox.checked);
    $.ajax({
        url:  '/correct_answer/',
        type: 'POST',
        data: {
            'pk' : id,
            'q_pk' : q_id,
            'is_correct' : checkbox.checked,
            'csrfmiddlewaretoken' : getCookie('csrftoken')
        },
    }).success(function(data) {
        console.log('http ' + data.status + ' ' + data.message);
        checkbox.setAttribute("checked", checkbox.checked);
    }).error(function() {
        console.log('http error');
    });
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
