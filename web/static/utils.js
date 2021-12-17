
function updateProgress() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("progressbar").style.width = scrolled + "%";
}

function scrollToPart(id){
  var node = document.getElementById(id);
  var yourHeight = 72;

  // scroll to your element
 // node.scrollIntoView(true);
  window.scroll(0, node.offsetTop - yourHeight);
  // now account for fixed header
  //var scrolledY = window.scrollY;

  //if(scrolledY){
  //  window.scroll(0, scrolledY - yourHeight);
  //}
}