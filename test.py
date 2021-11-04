from flask import Flask,render_template



app=Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/music/<path:filename>')
def download_file(CHAINS_oleg_vocal):
    return render_template('C:\Users\Оwen\Music', CHAINS_oleg_vocal)




if __name__ == "__main__":
    app.run(debug=True)