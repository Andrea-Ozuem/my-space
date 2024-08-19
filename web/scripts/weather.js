window.addEventListener("load", getWeather);

document.querySelector('.getWeather').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getWeather, handleErr);
    } else {
        alert('Geolocation is not supported by this browser.');
    } 
});

function getWeather(position) {
    if (position && position.coords) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        const WEATHER_KEY = CONFIG.WEATHER_KEY;
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${WEATHER_KEY}`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('frost').remove();
            const weather = document.getElementById('weather');
            weather.style.display = 'block';
            displayWeather(data);
        // Remove the button after fetching the weather
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
    }
}  

function displayWeather(data) {
    const desc = data.weather[0].description;
    const temp = data.main.feels_like;
    const humidity = data.main.humidity;
    const pressure = data.main.pressure;
    const speed = data.wind.speed;
    const city = data.name;

    if (city) document.querySelector('.city').innerHTML = `${city}`;
    if (speed) document.querySelector('.speed').innerHTML = `${speed} m/s`;
    if (temp) document.querySelector('.temp').innerHTML = `${temp} °C`;
    if (humidity) document.querySelector('.humid').innerHTML = `${humidity} %`;
    if (pressure) document.querySelector('.pressure').innerHTML = `${pressure} hpa`;
    if (desc) document.querySelector('.summ').innerHTML = `${desc}`;
}

function handleErr(error) {
    console.error('Geolocation error:', error.message);
    alert(`Error getting location: ${error.message}`);
}
  
// async function getWeather() {
//     let desc, temp, humidity, pressure, speed, city;

//     try {
//         [desc, temp, humidity, pressure, speed, city] = await geoFindMe();
//         if (city) document.querySelector('.city').innerHTML = `${city}`;
//         if (speed) document.querySelector('.speed').innerHTML = `${speed} m/s`;
//         if (temp) document.querySelector('.temp').innerHTML = `${temp} °C`;
//         if (humidity) document.querySelector('.humid').innerHTML = `${humidity} %`;
//         if (pressure) document.querySelector('.pressure').innerHTML = `${pressure} hpa`;
//         if (desc) document.querySelector('.summ').innerHTML = `${desc}`;
    
//         document.querySelector('.getWeather').style.display = 'none';
//     } catch (error) {
//         console.error("Failed to get weather data:", error);
//     }
// }

// async function geoFindMe() {
//     return new Promise((resolve, reject) => {
//         function success(position) {
//             const lat = position.coords.latitude;
//             const lon = position.coords.longitude;
//             const WEATHER_KEY = CONFIG.WEATHER_KEY;
//             const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${WEATHER_KEY}`;
//             console.log(lat, lon);
//             fetch(url)
//                 .then(response => {
//                     if (!response.ok) {
//                     if (response.status === 404) {
//                         throw new Error('Data not found');
//                     } else {
//                         throw new Error('Network response was not ok');
//                     }
//                     }
//                     return response.json();
//                 })
//                 .then(data => {
//                     // console.log(JSON.stringify(data, null, 2))
//                     console.log(data);
//                     const desc = data.weather[0].description;
//                     const temp = data.main.feels_like;
//                     const humidity = data.main.humidity;
//                     const pressure = data.main.pressure;
//                     const speed = data.wind.speed;
//                     const city = data.name
//                     // console.log(city)

//                     resolve([desc, temp, humidity, pressure, speed, city])
//                 })
//                 .catch(error => {
//                     reject(error);
//                 });
//             }
    
//         function error() {
//             reject("Unable to retrieve your location");
//         }
    
//         if (!navigator.geolocation) {
//             reject("Geolocation is not supported by your browser");
//         } else {
//             navigator.geolocation.getCurrentPosition(success, error);
//         }
//     });
// }
