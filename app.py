from flask import Flask,request,render_template
import pickle
import os

app=Flask(__name__)

database={'Owenzbs':'owenzbs','Solomia':'kuhar123','Peter':'Parker'}


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
	         return render_template('index.html', name=name1)

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/music',methods=['GET'])
def music():
    songs = os.listdir('static/music')
    return render_template("music.html", songs=songs)



if __name__ == "__main__":
    app.run(debug=True)