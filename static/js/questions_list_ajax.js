var since = 0;
var already = false;

function ajax_get_questions() {
    already = true;
    since += 10;
    $.ajax({
        url:  '/get_questions_list/',
        type: 'GET',
        data: {
            'since' : since,
            'tag' : search_text.value,
            'best' : best.value,
        },
    }).success(function(data) {
        questions_list.innerHTML += data;
            already = false;
    }).error(function() {
        error.style.visibility = 'visible';
        console.log('http error');
        already = false;
        since -= 10;
    });
}

window.onscroll = function() {
    var scrollHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight
    );
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    if (!already && scrollHeight - scrolled <= document.documentElement.clientHeight + 200) {
      ajax_get_questions();
    }
}
