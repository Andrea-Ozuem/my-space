$(document).ready(function () {
    let endpoint = 'https://api.linkpreview.net'
    let apiKey = 'e6073d242a72d509b55819a4e455fb5f'
    
    $.ajax({
        url: 'https://api.openweathermap.org/data/2.5/weather?q=' + "?key=" + apiKey + " &q=" + $( this ).text(),
        contentType: "application/json",
        dataType: 'json',
        success: function(result){
            console.log(result);
        }
    })
})

http://api.openweathermap.org/geo/1.0/direct?q=seattle&limit=1&appid=e6073d242a72d509b55819a4e455fb5f
