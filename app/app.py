#!/usr/bin/python3
from models import storage
from models.user import User
from models.tasks import Tasks
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def main():
    user = storage.get(User, id)
    tasks = user.tasks()
    return render_template('index.html',
                           name=name,
                           tasks=tasks)
# Research o using external apis in  flask app


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
