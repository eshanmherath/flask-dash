from datetime import datetime

from flask import Flask, render_template

from dash_server import dash_server

app = Flask(__name__)
app, create_secret = dash_server(app)


@app.route('/')
def home():
    dash_url = '/dash?secret={}'.format(create_secret('some value as key'))
    return render_template('home.html', dash_url=dash_url)


if __name__ == '__main__':
    app.run(debug=True)
