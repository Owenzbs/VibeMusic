from flask import Flask,request,render_template
import sqlite3
from mutagen.mp3 import MP3
import os
from flask_sqlalchemy import SQLAlchemy
import eyed3


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database={'Owenzbs':'owenzbs','Solomia':'kuhar123','Peter':'Parker'}

db=SQLAlchemy(app)
save_path = 'E:\Proggrams\project\static\music'

files=os.listdir("E:\Proggrams\project\static\music")
def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length 
    return str(hours),str (mins), str(seconds)

class musicstaff(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(1000), unique=True)
    duration = db.Column(db.String(1000), unique=True, nullable=False)
    artist = db.Column(db.String(1000))
    album = db.Column(db.String(1000))

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

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method=="POST":
        file=request.files["inputFile"]
        file.save(os.path.join(save_path, file.filename))
        song=f'E:\Proggrams\project\static\music\{file.filename}'
        track=eyed3.load(song)
        audio = MP3(song)
        audio_info=audio.info
        length = int(audio_info.length)
        hours, mins, seconds = audio_duration(length)
        newfile=musicstaff(name=str(track.tag.title), duration="{}:{}:{}".format(hours, mins, seconds), artist=str(track.tag.artist),album=str(track.tag.album))
        db.session.add(newfile)
        db.session.commit()
        
        
        
    return render_template("profile.html", message="Succesfully upload")

@app.route('/music',methods=['GET'])
def music():
    allsongs=musicstaff.query.order_by(musicstaff.id).all()
    songs = os.listdir('static/music')
    return render_template("music.html", songs=songs, allsongs=allsongs)

@app.route('/allmusic')
def allmusic():
    allsongs=musicstaff.query.order_by(musicstaff.id).all()
    return render_template("allmusic.html", allsongs=allsongs)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)