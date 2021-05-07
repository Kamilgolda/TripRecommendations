var price_key = document.getElementById("tripPrice").textContent
    var userk= document.getElementById("k2").textContent
    var tripk= document.getElementById("k1").textContent

var persons = document.getElementById("id_persons")
var users = document.getElementById("id_user")
var trip = document.getElementById("id_trip")
var price = document.getElementById("out")
var guide = document.getElementById("id_guide")
var room = document.getElementById("id_room")
var user= document.querySelector("#id_user").options
var trip= document.querySelector("#id_trip").options


    persons.oninput = getPrice;
    guide.oninput = getPrice;
    room.oninput = getPrice;

getPrice();


function getPrice()
{
    for(var i=0; i<user.length; i++) {

        if((user[i].text) == userk )
        {
            user.selectedIndex = 1
            console.log(user[i].text);
        }
    }

    for(var i=0; i< trip.length; i++) {

        if((trip[i].text) == tripk )
        {
            trip.selectedIndex = trip[i].value
            console.log(trip[i].text);
        }
    }
    //termin.value=termink.options[termink.selectedIndex].value
    var result= parseInt(persons.value) * parseInt(price_key)
    if(guide.checked)
        result += 300

    if(room.checked)
        result += 400

    if(isNaN(result))
        result = 0

    price.value=result

    var out=document.getElementById("out")

    out.innerText = result
}
