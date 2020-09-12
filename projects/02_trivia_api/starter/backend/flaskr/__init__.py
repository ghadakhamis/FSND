import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  questions_list = questions[start:end]

  return questions_list

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={"*" : {"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    # return data to view
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    total_records = len(questions)
    pagination_questions = paginate_questions(request, questions)
    categories = Category.query.all()
    # return data to view
    return jsonify({
      'success': True,
      'questions': pagination_questions,
      'total_questions': total_records,
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      # get the question by id
      question = Question.query.filter_by(id=id).one_or_none()
      # delete the question
      question.delete()
      # return success response
      return jsonify({
        'success': True,
        'questions_id': id
      })
    except:
      # abort if problem deleting question
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    question = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')
    if ((question is None) or (answer is None) or (difficulty is None) or (category is None)):
      abort(400)
    try:
      question = Question(question=question, answer=answer,difficulty=difficulty, category=category)
      question.insert()
      # get all questions and paginate
      questions = Question.query.order_by(Question.id).all()
      questions_list = paginate_questions(request, questions)
      categories = Category.query.all()

      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories},
        'questions': questions_list,
        'total_questions': len(questions)
      })
    except:
      # abort unprocessable if exception
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def get_filtered_questions():
    body = request.get_json()
    search_term = body.get('searchTerm')
    if (len(search_term) > 0):
      questions = Question.query.filter(Question.question.like("%{}%".format(search_term))).all()
    else:
      questions = Question.query.all()
    # paginate the results
    questions_list = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': questions_list,
      'total_questions': len(questions),
      'current_category': None
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_category_question(id):
    category = Category.query.filter_by(id=id).one_or_none()
    # abort 404 if category isn't found
    if (category is None):
      abort(404)
    questions = Question.query.filter_by(category=str(id)).all()
    # paginate the selection
    questions_list = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': questions_list,
      'total_questions': len(questions),
      'current_category': category.type
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def create_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions')
    quiz_category = body.get('quiz_category')
    # abort 400 if category or previous questions isn't exist
    if ((quiz_category is None) or (previous_questions is None)):
      abort(400)
    try:
      if (quiz_category['id'] == 0):
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        questions = Question.query.filter_by(category=quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()
      selected_question = questions[random.randrange(0, len(questions), 1)]
      if (selected_question is None):
        abort(404)
      return jsonify({
        'success': True,
        'question': selected_question.format()
      })
    except:
      # abort unprocessable if exception
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400
  
  return app

    