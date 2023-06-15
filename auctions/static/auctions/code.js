function updateTimer(endTime, timerId) {
  var endTimeMs = new Date(endTime).getTime();

  var updateInterval = setInterval(function () {
    var now = new Date().getTime();
    var distance = endTimeMs - now;

    if (distance <= 0) {
      clearInterval(updateInterval);
      document.getElementById(timerId).textContent = "Auction Ended";
    } else {
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      document.getElementById(timerId).textContent = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
    }
  }, 1000);
}
