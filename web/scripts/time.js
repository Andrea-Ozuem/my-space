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
    const awayTime = new Date().toLocaleString("en-US", { timeZone: "Asia/Manila" });
    time_away = new Date(awayTime);
    const hoursAway = time_away.getHours();
    const minsAway = time_away.getMinutes();
    const ampmAway = hoursAway >= 12 ? 'PM' : 'AM';

    away.innerHTML = `${hoursAway}:${minsAway} ${ampmAway}`;
}

updateTime();
