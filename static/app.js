let score = 0
$('#score').text(`Score: ${score}`)

let countdown = 60
const timer = setInterval(function() {
  $('#time').text(`Time remaining: ${countdown}`)
  countdown -= 1;

  if (countdown < 0) {
    clearInterval(timer);
    $('#submit-btn').on('click', function(event) {
      event.preventDefault();
      alert("Time's up!")
    })
    alert("Time's up!")
    async function saveScore() {
      const res = await axios.post('http://127.0.0.1:5000/save-score', { score });
      const scores = res.data.scores;
      const highestScore = scores.reduce(function(a, b) {
        return Math.max(a, b)
      });
      $('#highest-score').text(highestScore)
    }
    saveScore();
  }
}, 1000)

$('#guess-form').submit(async function(evt) {
  evt.preventDefault();
  $('.alert').remove();
  const $guess = $('#guess').val()
  const res = await axios.get('http://127.0.0.1:5000/check-word', {params: {guess: $guess}});
  $('#guess').val('')
  const message = res.data.result;

  if (message === "ok") {
    $('#message-container').append(`
    <div class="alert alert-success alert-dismissible fade show text-center mt-3" role="alert">
      <strong>You found one! ${$guess.length} points!</strong>
    </div>
    `)

    score += $guess.length;

    $('#score').text(`Score: ${score}`)
  } else if (message === "not-on-board") {
    $('#message-container').append(`
    <div class="alert alert-warning alert-dismissible fade show text-center mt-3" role="alert">
      <strong>Not on board.  Sorry, try again!</strong>
    </div>
    `)
  } else if (message === "not-a-word") {
    $('#message-container').append(`
    <div class="alert alert-danger alert-dismissible fade show text-center mt-3" role="alert">
      <strong>Not a word!  Try again!</strong>
    </div>
    `)
  }
})