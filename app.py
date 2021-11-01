from flask import Flask

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello bitch!"

@app.route('/about')
def about():
    return "We are trapper"

@app.route('/<name>')
def name(name):
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run()