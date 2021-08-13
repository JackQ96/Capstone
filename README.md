# Capstone

This is the final project for the Udacity Full Stack Web Development Nano Degree. 

Here we have created a movie reference application in which movie producers can upload details of movies and actors, these files can be viewed by casting agents who are looking for new talent for future projects.

### URL
https://git.heroku.com/capstone-jackq.git

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
#### Password: Casting1@udacity.com

## Endpoints

### GET Movies / Actors

The GET endpoints firstly will make sure the user is authorised by checking the JWT token and making sure it is valid. Once this has been confirmed the application allow the user to retrieve all information it has stored on either the Movies within the database or the Actors within the database.

### POST Movies / Actors

The POST endpoints (given the user has the authorization) will allow the user to create new entries and add new movies/actors to the existing database for everyone to see.

### PATCH Movies / Actors

The PATCH enpoints all the producers to make changes to the exisitng data within the database. This means if they made a mistake previously or an actors details have changed, they can seeemlessly update the database to rectify this issue. If a casting agent tried to do this they would be greeted with a 401 UNAUTHORIZED error.

### DELETE Movies / Actors

The DELETE endpoints are quite self explanatory and will allow the producer to delete any records that they no longer wish to be within the database. Once again, if a casting agent or any other user apart from the producer tried to do this, they would be greeted with a 401 UNAUTHORIZED error.
