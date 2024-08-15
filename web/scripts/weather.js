window.addEventListener("load", getWeather);

async function getWeather() {
    let desc, temp, humidity, pressure, speed, city;
    
    // if user.city, use city value to get location else
    try {
        [desc, temp, humidity, pressure, speed, city] = await geoFindMe();
    } catch (error) {
        console.error("Failed to get weather data:", error);
    }
    // populate html
    document.querySelector('.city').innerHTML = `${city}`;
    document.querySelector('.speed').innerHTML = `${speed} m/s`;
    document.querySelector('.temp').innerHTML = `${temp} °C`;
    document.querySelector('.humid').innerHTML = `${humidity} %`;
    document.querySelector('.pressure').innerHTML = `${pressure} hpa`;
    document.querySelector('.summ').innerHTML = `${desc}`;
}

function geoFindMe() {
    return new Promise((resolve, reject) => {
        function success(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const WEATHER_KEY = CONFIG.WEATHER_KEY;
            const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${WEATHER_KEY}`;
            
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                    if (response.status === 404) {
                        throw new Error('Data not found');
                    } else {
                        throw new Error('Network response was not ok');
                    }
                    }
                    return response.json();
                })
                .then(data => {
                    // console.log(JSON.stringify(data, null, 2))
                    const desc = data.weather[0].description;
                    const temp = data.main.feels_like;
                    const humidity = data.main.humidity;
                    const pressure = data.main.pressure;
                    const speed = data.wind.speed;
                    const city = data.name
                    // console.log(city)

                    resolve([desc, temp, humidity, pressure, speed, city])
                })
                .catch(error => {
                    reject(error);
                });
            }
    
        function error() {
            reject("Unable to retrieve your location");
        }
    
        if (!navigator.geolocation) {
            reject("Geolocation is not supported by your browser");
        } else {
            navigator.geolocation.getCurrentPosition(success, error);
        }
    });
}
