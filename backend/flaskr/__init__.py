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
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        # Set Access-Control-Allow
        response.headers.add('Access-Control-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    """
    All Route Handlers
    """

    @app.route('/categories')
    def get_categories():
        all_categories = Category.query.order_by(Category.type).all()

        if len(all_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in all_categories},
            'total_categories': len(all_categories)
        })

    @app.route('/questions')
    def get_questions():
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, all_questions)
        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        if categories is None:
            abort(404)

        return jsonify({
            'success': True,
            'total_questions': len(all_questions),
            'questions': current_questions,
            'categories': {category.id: category.type for category in categories},
            'current_category': None,
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category')
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question,
                                answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'new_question': question.id,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def seacrh_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', '')

        if len(search_term) == 0:
            abort(400)

        search_results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(
            search_term))).all()

        if len(search_results) == 0:
            abort(404)

        current_questions = paginate_questions(request, search_results)

        return jsonify({
            'success': True,
            'total_questions': len(search_results),
            'questions': current_questions,
            'current_category': None
        })

    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        try:
            current_category = Category.query.filter(Category.id == category_id).one_or_none()
            selection = Question.query.filter(Question.category == current_category.id).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': current_category.format()
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['GET', 'POST'])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category:
            if quiz_category['id'] == 0:
                quiz = Question.query.all()
            else:
                quiz = Question.query.filter_by(category=quiz_category['id']).all()

        selected = []
        for question in quiz:
            if question.id not in previous_questions:
                selected.append(question.format())

        if len(selected) != 0:
            result = random.choice(selected)
            return jsonify({
                'success': True,
                'question': result
            })

    '''
    All error handlers
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
    def invalid_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "invalid request"
        }), 400

    return app
