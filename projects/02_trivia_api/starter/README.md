# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

## Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
#### Running project

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Backend

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### API Reference

## Getting Started
Base URL: This application is hosted locally. The backend is hosted at http://localhost:5000/ and the frontend is hosted at http://localhost:3000/

## Error Handling
Errors are returned as JSON in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}
There are three types of errors which API will return one of them:

400 – bad request
404 – resource not found
422 – unprocessable

## Endpoints

# GET /categories
-Description: Returns a list categories.
-Full url: curl http://localhost:5000/categories
-Response:
  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
# GET /questions
-Description: Returns a list of pagination questions and list of categories.
-Full url: curl http://localhost:5000/questions
-Response:
  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "questions": [
          {
              "answer": "Test answer", 
              "category": 3, 
              "difficulty": 3, 
              "id": 164, 
              "question": "test question?"
          }
      ],
      "total_questions": 1,
      "success": true
  }
# DELETE /questions/<int:id>
-Description: delete question using it's id.
-Full url: curl http://localhost:5000/questions/1
-Response:
  {
      "questions_id": 1, 
      "success": true
  }
# GET /categories/<int:id>/questions
-Description: Get category using id and list of it's questions.
-Full url: curl http://localhost:5000/categories/1/questions
-Response:
{
      "current_category": "Science", 
      "questions": [
          {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
          }
      ], 
      "success": true, 
      "total_questions": 1
  }
# POST /quizzes
-Description: Allows users to play the quiz game.
-Full url: curl http://localhost:5000/quizzes
-Body: {"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'
-Response:
  {
      "question": {
          "answer": "test answer", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "test question?"
      }, 
      "success": true
  }
# POST /questions
-Description: allows users to create new question or saerch into question list 
-Full url: curl http://localhost:5000/questions
-Body: 
* case create question: { "question": "test question?", "answer": "test answer", "difficulty": 3, "category": "3" }
* case search into questions: {"searchTerm": "title"}
-Response:
* case create question:
 {
      "questions": [
          {
              "answer": "test", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "test?"
          }, 
          {
              "answer": "test", 
              "category": 5, 
              "difficulty": 4, 
              "id": 4, 
              "question": "test?"
          }
      ], 
      "success": true, 
      "total_questions": 2
  }
* case search into questions:
{
      "questions": [
          {
              "answer": "test", 
              "category": 6, 
              "difficulty": 3, 
              "id": 10, 
              "question": "test?"
          }
      ], 
      "success": true, 
      "total_questions": 1
  }

#### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

