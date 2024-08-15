document.addEventListener('DOMContentLoaded', function() {
    // if not logged in, redirect to login page
    if (!localStorage.getItem('accessToken')) {
        window.location.href = 'login.html';
    }

    // Set Authorization Header
    const accessToken = localStorage.getItem('accessToken');
    const headers = new Headers({
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    });

    // Set Name
    document.querySelector('.name').textContent = localStorage.getItem('name');

    let total = parseInt(document.querySelector('.total').textContent);
    if (total == 0) document.querySelector('.percent').textContent = 0;

    // Fetch tasks
    fetch('http://0.0.0.0:5001/api/v1/me/tasks', { headers })
        .then(response => response.json())
        .then(data => {
            const ul = document.getElementById('task-ul');
            document.querySelector('span.total').textContent = data.length;
            let done = 0;
            for (let task of data) {
                let li = document.createElement('li');
                if (task.completed) {
                    done ++;
                    li.innerHTML = `
                        <input type="checkbox" id="${task.id}" data-id="${task.id}" checked>
                        <label for="${task.id}">
                            <span class="custom-check"><i class="fa-solid fa-check"></i></span>
                            <p>${task.description}</p>
                        </label>`;
                } else {
                    li.innerHTML = `
                        <input type="checkbox" id="${task.id}" data-id="${task.id}">
                        <label for="${task.id}">
                            <span class="custom-check"><i class="fa-solid fa-check"></i></span>
                            <p>${task.description}</p>
                        </label>`;
                }
                ul.insertBefore(li, ul.firstChild);
            }
            document.querySelector('span.done').textContent = done;
            let percent = Math.floor(done / data.length * 100);
            document.querySelector('.percent').textContent = `${percent}%`;
        })
        .catch(error => {
            // console.error("Error retrieving todo:", error);
            alert(`Error: ${error.message || 'An unexpected error occurred.'}`);
        });

    // Task completes functionality
    document.getElementById('task-ul').addEventListener('change', function(event) {    
        let isChecked = event.target.checked;
        // let status = isChecked ? 1 : 0;
        let taskId = event.target.getAttribute('data-id');

        if (isChecked) {
            fetch(`http://0.0.0.0:5001/api/v1/tasks/${taskId}`, {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify({ completed: isChecked })
            })
            .then(response => response.json())
            .then(json => {
                // console.log(json)
                let done = parseInt(document.querySelector('.done').textContent);
                let total = parseInt(document.querySelector('.total').textContent);
                done = json.completed ? done + 1 : done - 1;
                document.querySelector('.done').textContent = done;
                let percent = Math.floor(done / total * 100);
                document.querySelector('.percent').textContent = `${percent}%`;
            })
            .catch(error => {
                alert(`Error: ${error.message || 'Error updating task'}`);
            });
        }
    });

    // Create new task
    document.querySelector('form.new-task').addEventListener('submit', function(event) {
        event.preventDefault();

        let todo = document.querySelector('.new');
        let data = {
            completed: false,
            description: todo.value
        };

        fetch(`http://0.0.0.0:5001/api/v1/me/tasks`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            const ul = document.getElementById('task-ul');
            const li = document.createElement('li');
            // document.querySelector('span.total').textContent += data.length;
            li.innerHTML = `
                <input type="checkbox" id="${data.id}" data-id="${data.id}">
                <label for="${data.id}">
                    <span class="custom-check"><i class="fa-solid fa-check"></i></span>
                    <p>${data.description}</p>
                </label>`;
            ul.insertBefore(li, ul.firstChild);
            let total = parseInt(document.querySelector('.total').textContent);
            document.querySelector('.total').textContent = total + 1;
        })
        .catch(error => {
            alert(`Error: ${error.message || 'An unexpected error occurred.'}`);
        });
        todo.value = "";
    });

    // Toggle Widgets
    document.querySelector('.wid-icon').addEventListener('click', function() {
        const widgets = document.querySelector('.widgets');
        if (widgets.classList.contains('pane')) {
            widgets.classList.remove('pane');
        } else {
            widgets.classList.add('pane');
        }
    });

    // clear functionality
    document.getElementById('clear').addEventListener('click', function(event) {
        event.preventDefault();
        const ul = document.getElementById('task-ul');
        const url = `http://0.0.0.0:5001/api/v1/tasks/clear`
        fetch(url, {
            method: 'DELETE',
            headers: headers
        })
        .then(() => {
            let count = 0;
            for (let li of ul.children) {
                console.log(li.children[0]);
                if (li.children[0].checked) {
                    count++;
                    li.remove();
                }
            }
            document.querySelector('.done').textContent = 0;
            let total = document.querySelector('.total').textContent;
            document.querySelector('.total').textContent = total - count;
        })
        .catch(error => {
            alert(`Error: ${error.message || 'Error clearing completed tasks'}`);
        });
    });
});

function deleteTask(taskId) {
    const url = `http://0.0.0.0:5001/api/v1/tasks/clear`
    fetch(url, {
        method: 'DELETE',
        headers: headers
    })
    .then(response => response.json())
    .catch(error => {
        alert(`Error: ${error.message || 'Error clearing completed tasks'}`);
    });
}
