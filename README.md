# Capstone

This is the final project for the Udacity Full Stack Web Development Nano Degree.

Here we have created a movie reference application in which movie producers can upload details of movies and actors, these files can be viewed by casting agents who are looking for new talent for future projects.

My motivation behind creating this app was to showcase the skills I have learned across the full stack of web development. I wanted to keep the application simple and easy to understand, whilst implementing features such as third party authentication and deploying the app live onto Heroku.




### URLs
#### Heroku: https://capstone-jackq3.herokuapp.com/
#### Auth0 Login: https://jackq.eu.auth0.com/authorize?audience=capstone&response_type=token&client_id=NB8Np9dSgNKoLQE9d9ssmnj9at6F8EfG&redirect_uri=https://127.0.0.1:5000/login-results

## Dependencies

Firslty please make sure you have python downloaded and up to date (Please refer to https://www.python.org/downloads/ for further info). 

After this, using pip in the terminal we can use:

```bash
pip install -r requirements.txt
```

to download all necessary requirements.

## Running the application

Firstly, with the terminal open, use the cd command to move into the corerct directory where you have saved the capstone folder. Once inside, use:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
to start up the server.

## Accounts

For test purposes i have created two seperate accounts, both with different levels of authorization. Firstly we have:

### Producer
The Producer has authorization to See/Edit/Post/Delete all Movies and Actors.

#### Login: Producer@udacity.com
#### Password: Producer1

### Casting Agent
The Casting Agent doesnt have the same level of authority within the app. The Agent can view all Movies and Actors but cannot make any changes to these files.

#### Login: Casting@udacity.com
#### Password: Casting1

## Endpoints

### GET Movies / Actors

The GET endpoints firstly will make sure the user is authorised by checking the JWT token and making sure it is valid. Once this has been confirmed the application allow the user to retrieve all information it has stored on either the Movies within the database or the Actors within the database. The output is of JSON format and is as follows:

```
             {
                  'success' : True,
                  'actors' : format_actors
             }
```

where format_actors is the list of actors present in the database that are all in the form of:

```
             {
                 'id': self.id,
                 'name': self.name,
                 'gender': self.gender,
                 'age': self.age
             }
```

### POST Movies / Actors

The POST endpoints (given the user has the authorization) will allow the user to create new entries and add new movies/actors to the existing database for everyone to see. Once the post endpoint is triggered, it will return the following(e.g. a new movie):

```
            {
                'success': True,
                'actor': new_movie.format()
            }
```
where new_movie.format() is the movie of the form:

```
           {
               'id': self.id,
               'title': self.title,
               'release_year': self.release_year,
               'genre': self.genre
           }
```
### PATCH Movies / Actors

The PATCH enpoints all the producers to make changes to the exisitng data within the database. This means if they made a mistake previously or an actors details have changed, they can seeemlessly update the database to rectify this issue. If a casting agent tried to do this they would be greeted with a 401 UNAUTHORIZED error. This process is done retrieving the current data from the database and once found, the api will overwrite the data and update the database. Once the movie/actor has been updated you will receive the confirmation output of:

```
          {
               'success': True,
               'changed_actor': format_edited_actor
          }
```

### DELETE Movies / Actors

The DELETE endpoints are quite self explanatory and will allow the producer to delete any records that they no longer wish to be within the database. Once again, if a casting agent or any other user apart from the producer tried to do this, they would be greeted with a 401 UNAUTHORIZED error. The API will first query the database and find the correct record (checking the records ID) and then remove the record from the database before updating. Once this is done it will return:

```
         {
               'success': True,
               'deleted_actor': format_actor
         }
```
as confirmation that the file has been succesfully deleted.
