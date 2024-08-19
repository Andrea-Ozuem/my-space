document.querySelector('.auth').addEventListener('submit', function(event) {
    event.preventDefault();

    if (document.getElementById('login')) {
        const url = 'http://localhost:5001/auth/login';
        redirectHome(event, url);
    } else if (document.getElementById('signup')) {
        const url = 'http://localhost:5001/auth/register';
        redirectHome(event, url);
    }
});

function redirectHome(event, url) {
    const formData = new FormData(event.target);
    const jsonData = {};
    formData.forEach((value, key) => {
      jsonData[key] = value;
    });

    // Send JSON data using Fetch API
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jsonData),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('accessToken', data.data.access_token);
        localStorage.setItem('name', data.data.user.first_name);
        localStorage.setItem('city', data.data.user.city);
        localStorage.setItem('lastName', data.data.user.last_name);
        localStorage.setItem('tz', data.data.user.tz1);
        window.location.href = 'index.html';
    })
    .catch(error => {
        alert(`Error: ${error.error || 'An unexpected error occurred.'}`);
    });
}
