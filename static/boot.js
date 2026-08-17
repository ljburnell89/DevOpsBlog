(function(){
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bootLines = [
    "booting alam@blog ...",
    "mounting /posts ................ [ok]",
    "loading fonts ................... [ok]",
    "starting shell ................... [ok]",
    ""
  ];
  var bootEl = document.getElementById('boot');
  var pageBody = document.getElementById('page-body');

  function reveal(){ if (pageBody) pageBody.classList.remove('hidden'); }

  function typeBoot(){
    if (!bootEl){ reveal(); return; }
    if (reduceMotion){
      bootEl.textContent = bootLines.join('\n');
      reveal();
      return;
    }
    var full = bootLines.join('\n');
    var i = 0;
    bootEl.innerHTML = '<span class="cursor"></span>';
    var interval = setInterval(function(){
      i++;
      bootEl.textContent = full.slice(0, i);
      if (i >= full.length){
        clearInterval(interval);
        reveal();
      }
    }, 10);
  }

  function tickClock(){
    var el = document.getElementById('status-clock');
    if(!el) return;
    var now = new Date();
    var pad = function(n){ return String(n).padStart(2,'0'); };
    el.textContent = pad(now.getHours()) + ':' + pad(now.getMinutes()) + ':' + pad(now.getSeconds());
  }

  typeBoot();
  tickClock();
  setInterval(tickClock, 1000);
})();
