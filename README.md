# Udacity captone project - Casting agency

This project is the final project of Udacity Full Stack Developer Nano Degree Program.
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server locally

From within the `/beckend` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

The following two commands export neccessary environment variables for the program.

```bash
chmod +x setup.sh
source setup.sh
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Authentication

The project uses Auth0 as a third-party authentication system. 
The bearer tokens needed for running the api are saved in setup.sh file but they may be expired.
To generate new valid tokens: go to https://dev-4xm89r5o.us.auth0.com/authorize?audience=capstone_login&response_type=token&client_id=8s5THOjrKG8B7npwzi0t4KfHyopyxJMc&redirect_uri=http://127.0.0.1:5000/actors to get corresponding tokens:
  - To get bearer token of Casting Assistant:
     login account: Casting_Assistant@outlook.com 
           passwaord:saltywater9707!
  - To get bearer token of Casting Director:
     login account: Casting_Director@outlook.com 
           passwaord:saltywater9707!
  - To get bearer token of Executive Producer:
     login account: Executive Producer@outlook.com 
           passwaord:saltywater9707!
If you want to use your own Auth0 account, you can go to https://auth0.com/ and create an API for this program.(Do not forget to replace these parameters in setup.sh
with yours)

## Deployment

The API is also running lively on https://myapp-capstone-970719.herokuapp.com/ supported by heroku.

You can login with different accounts with different permissions. Those accounts are mentioned in Authentication section above.


## API

### Endpoints

#### GET /actors

GET '/actors'
- Fetches all actors
- Request Arguments: None
- Returns: An jason object with keys: 'success' and 'actors'. 'movies' key contains all actor objects exsiting in database.
- example response:
```json
{
  "actors": [
    {
      "id": 1,
      "name": "actor_1",
      "age": 20,
      "gender": "male"
    },
    {
      "id": 1,
      "name": "actor_2",
      "age": 20,
      "gender": "female"
    }
  ],
  "success": true
}
```

#### GET /movies

GET '/movies'
- Fetches all movies
- Request Arguments: None
- Returns: An jason object with keys: 'success' and 'movies'. 'movies' key contains all movie objects exsiting in database.
- example response:
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2022-1-1",
      "title": "title_1"
    },
    {
      "id": 2,
      "release_date": "2022-1-2",
      "title": "title_2"
    }
  ],
  "success": true
}
```

#### DELETE /actors/<int:id\>

DELETE '/actors/${id}'
- Deletes a specified actor using the id of the actor
- Request Arguments: id - integer
- Returns: a jason object:
```
{
  "success": True,
  "deleted id": id
}
```

#### DELETE /movies/<int:id\>

DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
- Request Arguments: id - integer
- Returns: a jason object:
```
{
  "success": True,
  "deleted id": id
}
```

#### POST /actors
- Sends a post request in order to post an new actor
- Request Body: a jason object of the new actor
```
{
  "name": "new_actor",
  "age": 20,
  "gender": "female",
}
```
- Returns: a jason object refelcting the name of the newly added actor
```
{
  "success": true,
  "name": "new_actor"
}
```

#### POST /movies
- Sends a post request in order to post an new movie
- Request Body: a jason object of the new movie
```
{
  "title": "new_title",
  "release_data": "2022-11-1"
}
```
- Returns: a jason object refelcting the title of the newly added actor
```
{
  "success": True,
  "title": "new_title"
}
```

#### PATCH /actors/\<int:id\>

- Sends a patch request in order to edit a specified actor based on the actor's id
- Request Arguments: id - integer, which is the id of the actor
- Request Body: a jason object containing parameters to edit
```
{
  "name": "name_to_edit",
  "age": None,
  "gender": None,
}
```
- Returns: a jason object refelcting the name of the edited actor
```
{
  "success": True,
  "name": "actor_edited"
}
```

#### PATCH /movies/\<int:id\>

- Sends a patch request in order to edit a specified movie based on the movie's id
- Request Arguments: id - integer, which is the id of the movie
- Request Body: a jason object containing parameters to edit
```
{
  "title": "title_to_edit",
  "release_date": None
}
```
- Returns: a jason object refelcting the name of the edited actor
```
{
  "success": True,
  "title": "movie_edited"
}
```

## How to run the tests

Firstly, you need to create a new test database in your local postgresql
```
create database capstone_test;
```
Replace DATABASE_TEST_URL in setup.sh with your own DATABASE_TEST_URL
Run tests
```
python test_app.py
```
