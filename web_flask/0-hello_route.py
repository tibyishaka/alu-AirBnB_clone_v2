#!/usr/bin/python3
# Print Hello HBNB! with Flask framework
from flask import Flask
app = Flask(_name_)


@app.route('/', strict_slashes=False)
def hello():
    """Print Hello HBNB!
    """
    return 'Hello HBNB!'

if name == 'main':
    app.run(host='0.0.0.0', port=5000)
