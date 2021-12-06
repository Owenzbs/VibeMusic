from re import I
from flask import Flask,request,render_template
import sqlite3
from mutagen.mp3 import MP3
import os
from flask_sqlalchemy import SQLAlchemy
import eyed3


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSH_BASE'] ='whoosh'


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

class users(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(1000), unique=True)
    username = db.Column(db.String(1000), unique=True)
    password= db.Column(db.String(1000), unique=True)



@app.route('/')
def index():
    return render_template("playlist.html")


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method=="POST":
        userstaff=users.query.order_by(users.id).all()
        email=request.form.get("email1")
        for i in userstaff:
            if str(email)==str(i.email):
                return render_template("register.html", message="Email already exists")
        checkpassword=request.form.get("password1")
        password=request.form.get("password")
        name=request.form.get("text")
        if str(checkpassword) != str(password):
            return render_template("register.html", message="Incorect password")
        checkbox1=request.form.get("checkbox1")
        if checkbox1==None:
            return render_template("register.html", message="Agree wtih a terms!")
        checkbox2=request.form.get("checkbox2")
        if checkbox2==None:
            return render_template("register.html", message="Agree wtih a terms!")
        newfile=users(email=str(email), username=str(name), password=str(password))
        db.session.add(newfile)
        db.session.commit()
    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get("useremail")
        password=request.form.get("userpassword")
        userstaff=users.query.order_by(users.id).all()
        checkbox123=request.form.get("checkbox123")
        if str(checkbox123)=="None":
            return render_template("login.html", message="Agree wtih a terms!")
        for el in userstaff:
            if str(el.email) == str(email):
                if str(el.password) == str(password):
                    return render_template('profile.html')
        for i in userstaff:        
            if str(i.email) != str(email):
                return render_template("login.html", message="Incorrect email")
            if str(i.password) != str(email):
                return render_template("login.html", message="Incorrect password")
        
    return render_template("login.html")

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
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    for i in allsongs:
        for el in songs:
            if i.name in str(el):
                list1.append(i.id)
                list2.append(el)
                list3.append(i.duration)
                list4.append(i.artist)
                list5.append(i.album)
    return render_template("music.html", count=len(songs),   songs=songs, allsongs=allsongs, list1=list1, list2=list2, list3=list3 , list4=list4, list5=list5)

#@app.route('/allmusic')
#def allmusic():
#    allsongs=musicstaff.query.order_by(musicstaff.id).all()
#    return render_template("allmusic.html", allsongs=allsongs)

@app.route('/search', methods=['POST','GET'])
def search():
    title=request.form.get("title")
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    allsongs=musicstaff.query.order_by(musicstaff.id).all()
    songs = os.listdir('static/music')
    if request.method=="POST":
        for i in allsongs: 
            if (title in i.name) :   
                for el in songs:
                    if (title in el) :
                        list1.append(i.id)
                        list2.append(el)
                        list3.append(i.duration)
                        list4.append(i.artist)
                        list5.append(i.album)
        
    return render_template("allmusic.html", allsongs=allsongs, songs=songs, count=len(list1), result1=list1, result2=list2, result3=list3, result4=list4, result5=list5)
    


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)