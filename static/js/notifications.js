var channel_id = $("div#channel_id").html();  // opened question id
var ws = new WebSocket("ws://localhost:8888/ws/" + channel_id);

ws.onmessage = function(ev){
  // console.log("GOT");
  // var json = JSON.parse(ev.data);
  // var new_ans = '<a name="answer_' + json.id + '"></a><div class="row question__block fresh"><div class="col-xs-2 question__left"><img class="img-rounded question__avatar" src="/uploads/' + json.avatar + '"><div id="' + json.id + '" class="rating__info answer_rating">Rating: 0</div><div class="fresh__like"><span id="' + json.id + '" class="like__button ans_like">+</span><span id="' + json.id + '" class="like__button ans_dislike">-</span></div></div><div class="col-xs-10 question__right"><p>' + json.text + '</p><div class="question__tags"><strong>Author:</strong> ' + json.nickname + ' </div></div></div><br>';
  $('div#fresh_answers').append(ev.data);
};
