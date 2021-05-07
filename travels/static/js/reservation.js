var price_key = document.getElementById("tripPrice").textContent

var persons = document.getElementById("id_persons")
var price = document.getElementById("price_form")
var guide = document.getElementById("id_guide")
var room = document.getElementById("id_room")
var all_inclusive = document.getElementById("id_all_inclusive")


    persons.oninput = getPrice;
    guide.oninput = getPrice;
    room.oninput = getPrice;
    all_inclusive.oninput = getPrice;

getPrice();


function getPrice()
{
    var result= parseInt(persons.value) * parseInt(price_key)
    if(guide.checked)
        result += 700

    if(room.checked)
        result += 400

    if(all_inclusive.checked)
        result += 500

    if(isNaN(result))
        result = 0

    price.innerText = result
}
