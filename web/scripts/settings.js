const fname = localStorage.getItem('name');
const lname = localStorage.getItem('lastName');
const city = localStorage.getItem('city');
const tz = localStorage.getItem('tz');

const accessToken = localStorage.getItem('accessToken');
const headers = new Headers({
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
});

document.getElementById('fname').setAttribute('value', fname);
document.getElementById('lname').setAttribute('value', lname);
document.getElementById('city').setAttribute('value', city);

const timeZones = Intl.supportedValuesOf('timeZone')
timeZones.forEach(timeZone => {
    const option = document.createElement('option');

    if (timeZone === tz) {
        option.selected;
    }
    option.value = timeZone;
    option.text = timeZone;
    document.getElementById('tz1').appendChild(option);
});

document.querySelector('form').addEventListener('submit', (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const formJSON = Object.fromEntries(formData.entries());

    fetch('http://localhost:5001/api/v1/me/update',  {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify(formJSON),
    })
    .then(response => {
        if (response.ok) return response.json();
        throw new Error('Error Updating Settings');
    })
    .then(data => {
        // console.log(data);
        localStorage.setItem('name', data.first_name);
        localStorage.setItem('city', data.city);
        localStorage.setItem('tz', data.tz1);
        localStorage.setItem('lastName', data.last_name);

        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error(error);
        alert('Error Updating Settings');
    });
});