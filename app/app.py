#!/usr/bin/python3
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template
import os


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def main():
    user = storage.get(User, '00a11245-12fa-436e-9ccc-967417f8c30a')
    if os.getenv('STORAGE_TYPE', None) == 'db':
        tasks = user.tasks
    else:
        tasks = user.tasks()
    done = [task for task in tasks if task.completed == 1]
    return render_template('index.html',
                           name=user.first_name,
                           tasks=tasks, total=len(tasks),
                           done=len(done))

# Research o using external apis in  flask app


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
