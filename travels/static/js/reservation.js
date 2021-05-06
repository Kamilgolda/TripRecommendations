var user_key = document.getElementById("k2").textContent
var trip_key = document.getElementById("k1").textContent
var price_key = document.getElementById("k3").textContent

var persons = document.getElementById("id_persons")
var user = document.getElementById("id_user")
var trip = document.getElementById("id_trip")
var price = document.getElementById("id_price")
var guide = document.getElementById("id_guide")
var room = document.getElementById("id_room")

    persons.oninput = getPrice;
    guide.oninput = getPrice;
    room.oninput = getPrice;

getPrice();

function getPrice()
{

    user.value= 1
    trip.value= 1
    //termin.value=termink.options[termink.selectedIndex].value
    var result= parseInt(persons.value) * price_key

    if(guide.checked)
        result += 300

    if(room.checked)
        result += 400

        price.value=result

    var out=document.getElementById("out")

    out.innerText = result
}
