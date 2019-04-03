

function getWindowSize() {
  var h;

  if(typeof document.compatMode != 'undefined' && document.compatMode == 'CSS1Compat') {
      h = document.documentElement.clientHeight;
  } else if(typeof document.body != 'undefined' && (document.body.scrollLeft || document.body.scrollTop)) {
      h = document.body.clientHeight;
  }

  return h;
}

function getsize(){
  var size = getWindowSize();
  //document.getElementById("body1").value = size.x;
  document.getElementById("body1").style.height= size-20+"px";
}

window.onload = function(){
 var currentHeight = document.documentElement.clientHeight; 	  
 var body1 = document.getElementById("body1");
 body1.style.height= currentHeight-20+"px";
 placeholderPic();
}
function transform(  a){
  if(a==1)
  {
    window.location="./add.html";
  }
  else if(a==2)
  {
    window.location="./delete.html";
  }
  else if(a==3)
  {
    window.location="./update.html";
  }
  else if(a==4)
  {
    window.location="./select.html";
  }
  else if(a==5)
  {
    window.location="./homepage.html";
  }
}
function placeholderPic(){
    var w = document.documentElement.offsetWidth;
    var m=w/1519*2*100;
  var n=w/1519*4*100;
  var k=w/1519*1*100;
  for(var i=0;i<4;++i)
  {
    /*alert(m);*/
    document.getElementsByTagName("li")[i].style.fontSize=m+"%";
  }
    document.getElementsByTagName("h1")[0].style.fontSize=n+"%";
    document.getElementsByTagName("h1")[0].style.lineHeight=k+"%";
    document.getElementsByClassName("tip")[0].style.fontSize=k+"%";
    document.getElementById("readme").style.fontSize=k+"%";
    document.getElementById("time").style.fontSize=k+"%";
    document.getElementById("time1").style.fontSize=k+"%";
    document.getElementById("copyrightWords").style.fontSize=k+"%";
    document.getElementById("log").style.height=k*0.0845+"%";
   }

   window.onresize=function(){
    placeholderPic();
   }
