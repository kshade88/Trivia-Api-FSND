# Full Stack Trivia!

## Introduction
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the 
idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game.

Now that the backend API is completed, the application will:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
Below is a set of instructions to run the application on your own machine. It is encouraged to set up the backend 
before moving onto the front end.
- Python 3.7 or later is required, refer to [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) for installation and uppdating.
- Set up a virtual enviorment before installing dependencies (recomended).
### Backend Setup
- Navigate to the `/backend` directory of your trivia api application.
- Install dependencies with `pip install -r requirements.txt` (use pip3 instead if needed).
- Run `psql trivia < trivia.sql` from the backend directory to restore the database dumped into the trivia.psql file.
- To run the server, execute the following from the backend directory: 

Set flaskr as the flask app:
  `export FLASK_APP=flaskr`
Run Flask:
  `flask run --reload`

### Frontend
- Project depends on Nodejs and NPM. You can download them from [here](https://nodejs.org/en/download/).
- Navigate to the `/frontend` directory.
- Install npm with `install npm`.
- Run the frontend with `npm start`.

## Resource Endpoint Library
This is a library of all expected endpoints and their behaviors.

### GET `/categories`
- Fetches a dictionary of all categories with ids as the keys and type as the value.
- Request Arguments: None
- Expected Return:
```js
{'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"}
  }
```  
  
### GET `/questions?page={integer}`
- Fetches a paginated set of 10 questions, total number of questions, and all categories 
- Request Arguments: page - integer 
- Expected Return:
```js
{
    "categories": {
        "1":"Science", 
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
        },
    "current_category":null, 
    "questions":[
        {
            "answer":"sample answer",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"sample question"},],
    "success":true,
    "total_questions":27
}
```

### GET `/categories/{id}/questions`
- Fetches all questions for a specific category by a particular catgeory id
- Request Arguments: id - integer
- Expected Return:
```js
{
    "current_category":{
        "id":1,
        "type":"Science"},
    "questions":[
        {
            "answer":"The Liver",
            "category":1,
            "difficulty":4,
            "id":20,
            "question":"What is the heaviest organ in the human body?"},
    "success":true,
    "total_questions":3}
```

### DELETE `/questions/{id}`
- Deletes a specified question by its specific question id.
- Request Arguments: id - integer
- Expected Return:
```js
{           
    'success': True,       
    'deleted': {id},
}                        
```                       

### POST `/quizes`
- Send a post request in order to retrive a single question from a pool of unasked questions either in a specific 
  category or from all categories.
- Required body arguments: Previous questions as array of question ids and current category by category id. ID of 
  zero equates to all categories. 
- Example body:
```js
{'previous_questions': [1, 3, 6], 'quiz_category': [5]}
```
- Expected Return:
```js
{
    'success': True, 
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 5
  }
}
```

### POST `/questions`
- Adds a new question to the questons database table.
- Request body example:
```js
{
    'question':  'sample new question?',
    'answer':  'sample new answer!',
    'difficulty': 1,
    'category': 3,
}
```
- Expected Return:
```js
{                             
    'success': True,                            
    'new_question': {id},                
    'total_questions': 14,
}                                             
```

### POST `/questions`
- Searches and filters through all questions using a POST request and a search term argument.
- Required Arguments: searchTerm - String
- Expected Return:
```js
{
    'success': True, 
    'total_questions': 6,
    'questions': [{
        'question': 'sample new question?',
        'answer': 'sample new answer!',
        'difficulty': 1,
        'category': 3,
  }],
    'current_category': None
}
```