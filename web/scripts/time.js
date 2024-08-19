setInterval(updateTime, 1000);

function updateTime() {
    const home = document.querySelector('#home-time');
    const away = document.querySelector('#away-time');

    // Home time
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    home.innerHTML = `${hours}:${minutes} ${ampm}`;

    // away time
    let tz1;
    if (localStorage.getItem('tz')) {
        tz1 = localStorage.getItem('tz')
    } else {
        tz1 = 'Europe/Paris';
    }
    const awayTime = new Date().toLocaleString("en-US", { timeZone: tz1 });
    time_away = new Date(awayTime);
    const hoursAway = time_away.getHours();
    const minsAway = time_away.getMinutes();
    const ampmAway = hoursAway >= 12 ? 'PM' : 'AM';

    document.getElementById('away').textContent = tz1;
    away.innerHTML = `${hoursAway}:${minsAway} ${ampmAway}`;
}

updateTime();
