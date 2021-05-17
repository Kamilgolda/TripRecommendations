var x = window.location.href;
var b1 = document.getElementById("b1")
var b2 = document.getElementById("b2")
var b3 = document.getElementById("b3")
if (b1.href == x) {b1.classList.add("active");}
if (b2.href == x) {b2.classList.add("active");}
if (b3.href == x) {b3.classList.add("active");}
