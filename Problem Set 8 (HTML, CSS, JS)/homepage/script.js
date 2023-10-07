function init() {
  console.log("init call");

  setTimeout(function() {
    console.log("set timer call");
  }, 3000);



  $("#yes").click(function() {
    hidePop();
  });

  $("#no").click(function() {
    hidePop();
  });


}

function hidePop() {
  animate("#popup",10,-275);
}


function animate(sel, startingPos, endPos) {
  var elem = $(sel);
  var pos = startingPos;
  var id;


  id = setInterval(function() {
        console.log("running");
    if (pos <= endPos) {
        console.log("stopped");
      clearInterval(id);
    } else {
      pos-=5;


      elem.css({right: pos})
    }
  }, 10);

}





$(document).ready(function() {
  init();
});
