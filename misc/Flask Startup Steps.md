# Flask Startup Steps

## Setup Steps

1. Added FLASK_ENV=development to vscode setting in vscode's settings.json file:
    - "terminal.integrated.env.windows": {
        "FLASK_ENV": "development"
    },
2. Initialize git and set up remote (if necessary).
3. Create virtual environment:
    - python -m venv venv
4. Start using virtual environment
    - venv\Scripts\activate.bat  (windows)
5. Install flask
    - pip install flask
    - select proper Python environment.  Click on Python lower left toolbar. Select  python 3.7.7 64bit (‘venv’)
6. Install debugtoolbar
    - pip install flask-debugtoolbar
7. Create requirements.txt file:
    - pip freeze > requirements.txt  (re-create with each installation)
8. Create .gitignore file
9. Add code to app.py file:
    - `from flask import Flask, request, render_template`
      - may run into "unresolved import 'Flask'" linting error. To solve: F1 and then Python: Select Interpreter. Select 64 bit ('venv'). May have to restart vscode.
    - `from flask_debugtoolbar import DebugToolbarExtension`
    - `app=Flask(__name__)`
    - `app.config[‘SECRET_KEY’]=”secret-phrase”`
    - `debug = DebugToolbarExtension(app)`
10. flask run
11. Deactivate virtual environment
    - Deactivate

## Directory Structure

- project-directory
  - templates
    - base.html
    - view.html
  - static
    - app.css
    - app.js
  - venv
  - app.py
