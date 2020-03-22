from flask import Flask, render_template, request
import sqlite3  
import requests





app = Flask(__name__)
@app.route('/')
def homepage():  
    params = {
    'api_key': 'cf542155',
    'OMDBapi': 'dc626e14',
  }
    r = requests.get(
      'http://omdbapi.com/',
      params=params)
    return render_template('movies.html')

@app.route("/")  
def index():  
    return render_template("index.html");  
 
@app.route('/login',methods = ["GET","POST"])  
def login():  
    error = None;  
    if request.method == "POST":  
        if request.form['pass'] != 'jtp':  
            error = "invalid password"  
        else:  
            flash("you are successfuly logged in")  
            return redirect(url_for('home'))  
    return render_template('login.html',error=error)    
 
@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:
            title = request.form['Title'],
            year=request.form['Year'],
            runtime=request.form['Runtime'],
            genre=request.form['Genre'],
            director=request.form['Director'],
            cast=request.form['Actors'],
            writer=request.form['Writer'],
            language=request.form['Language'],
            country=request.form['Country'],
            awards=request.form['Awards'],
            imdb_rating=request.form['imdbRating'],
            imdb_votes=request.form['imdbVotes'],
            box_office=request.form['BoxOffice']
            with sqlite3.connect('movies.sqlite') as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Movies (Title, Year, Runtime, Genre, Director, Actors, Writer, Language, Country, Awards, imdbRating, imdbVotes, BoxOffice) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",(title, year, runtime, genre, director, cast,writer, language, country, awards, imdb_rating, imdb_votes, box_office ))  
                con.commit()  
                msg = "Movie successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the movie to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  

 

@app.route("/view")  
def view():  
    con = sqlite3.connect('movies.sqlite')  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from MOVIES")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  

 
 
@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    cls = request.form["id"]  
    with sqlite3.connect('movies.sqlite') as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Movie where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)  
  
if __name__ == "__main__":  
    app.run(debug = True)  