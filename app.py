import urllib.request, urllib.parse, urllib.error
import json
import os
import sqlite3


#Get API key
with open('APIkeys.json') as f:
    keys = json.load(f)
    omdbapi = keys['OMDBapi']

#URL from where to get movie information    
serviceurl = 'http://www.omdbapi.com/?'
apikey = '&apikey='+omdbapi    

#Function for printing a JSON dataset
def print_json(json_data):
    list_keys=['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 
               'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings', 
               'Metascore', 'imdbRating', 'imdbVotes', 'imdbID']
    print("-"*50)
    for k in list_keys:
        if k in list(json_data.keys()):
            print(f"{k}: {json_data[k]}")
    print("-"*50)

#Function to download a poster of the movie based on the information from the jason dataset
#Saves the downloaded poster in a local directory called 'Posters'

def save_poster(json_data):
    import os
    title = json_data['Title']
    poster_url = json_data['Poster']
    # Splits the poster url by '.' and picks up the last string as file extension
    poster_file_extension=poster_url.split('.')[-1]
    # Reads the image file from web
    poster_data = urllib.request.urlopen(poster_url).read()
        
    savelocation=os.getcwd()+'\\'+'Posters'+'\\'
    # Creates new directory if the directory does not exist. Otherwise, just use the existing path.
    if not os.path.isdir(savelocation):
        os.mkdir(savelocation)
    
    filename=savelocation+str(title)+'.'+poster_file_extension
    f=open(filename,'wb')
    f.write(poster_data)
    f.close()

#Function to create/update the local movie database with the data retreived from the web
#Saves the movie data (Title, Year, Runtime, Country, Metascore, and IMDB rating) into a local SQLite database called 'movieinfo.sqlite'

def save_in_database(json_data):
    
    filename = input("Please enter a name for the database (extension not needed, it will be added automatically): ")
    filename = filename+'.sqlite'
    
    import sqlite3
    conn = sqlite3.connect(str(filename))
    cur=conn.cursor()
    
    title = json_data['Title']
    # Goes through the json dataset and extracts information if it is available
    if json_data['Year']!='N/A':
        year = int(json_data['Year'])
    if json_data['Runtime']!='N/A':
        runtime = int(json_data['Runtime'].split()[0])
    if json_data['Country']!='N/A':
        country = json_data['Country']
    if json_data['Metascore']!='N/A':
        metascore = float(json_data['Metascore'])
    else:
        metascore=-1
    if json_data['imdbRating']!='N/A':
        imdb_rating = float(json_data['imdbRating'])
    else:
        imdb_rating=-1
    
    # SQL commands
    cur.execute('''CREATE TABLE IF NOT EXISTS MovieInfo 
    (Title TEXT, Year INTEGER, Runtime INTEGER, Country TEXT, Metascore REAL, IMDBRating REAL)''')
    
    cur.execute('SELECT Title FROM MovieInfo WHERE Title = ? ', (title,))
    row = cur.fetchone()
    
    if row is None:
        cur.execute('''INSERT INTO MovieInfo (Title, Year, Runtime, Country, Metascore, IMDBRating)
                VALUES (?,?,?,?,?,?)''', (title,year,runtime,country,metascore,imdb_rating))
    else:
        print("Record already found. No update made.")
    
    # Commits the change and close the connection to the database
    conn.commit()
    conn.close()


#Function to print contents of the local database
def print_database(database):
    
    import sqlite3
    conn = sqlite3.connect(str(database))
    cur=conn.cursor()
    
    for row in cur.execute('SELECT * FROM MovieInfo'):
        print(row)
    conn.close()
    
#Function to save the database content in an Excel file
def save_in_excel(filename, database):
    
    if filename.split('.')[-1]!='xls' and filename.split('.')[-1]!='xlsx':
        print ("Filename does not have correct extension. Please try again")
        return None
    
    import pandas as pd
    import sqlite3
    
    #df=pd.DataFrame(columns=['Title','Year', 'Runtime', 'Country', 'Metascore', 'IMDB_Rating'])
    
    conn = sqlite3.connect(str(database))
    #cur=conn.cursor()
    
    df=pd.read_sql_query("SELECT * FROM MovieInfo", conn)
    conn.close()
    
    df.to_excel(filename,sheet_name='Movie Info')
    
#Function to search for information about a movie    
def search_movie(title):
    if len(title) < 1 or title=='quit': 
        print("Goodbye now...")
        return None

    try:
        url = serviceurl + urllib.parse.urlencode({'t': title})+apikey
        print(f'Retrieving the data of "{title}" now... ')
        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data=json.loads(data)
        
        if json_data['Response']=='True':
            print_json(json_data)
            
            # Asks user whether to download the poster of the movie
            if json_data['Poster']!='N/A':
                poster_yes_no=input ('Poster of this movie can be downloaded. Enter "yes" or "no": ').lower()
                if poster_yes_no=='yes':
                    save_poster(json_data)
            # Asks user whether to save the movie information in a local database
            save_database_yes_no=input ('Save the movie info in a local database? Enter "yes" or "no": ').lower()
            if save_database_yes_no=='yes':
                save_in_database(json_data)
            return 1
        else:
            print("Error encountered: ",json_data['Error'])
    
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}")    
        
#Search for ''        
title = input('\nEnter the name of a movie (enter \'quit\' or hit ENTER to quit): ')
if len(title) < 1 or title=='quit': 
    print("Goodbye now...")
else:
    search_movie(title)     
    
#Show the downloaded poster of ''
from IPython.display import Image
Image("Posters/Titanic.jpg")       

#Print the content of the local database
print_database('movies.sqlite')


#app.run(debug=True)




