import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format( self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question':'This is the question',
            'answer':'This is the answer',
            'category': 2,
            'difficulty': 3
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['question']['question'], self.new_question['question'])
        self.assertEqual(data['question']['answer'], self.new_question['answer'])
        self.assertEqual(data['question']['category'], self.new_question['category'])
        self.assertEqual(data['question']['difficulty'], self.new_question['difficulty']) 

    def test_search_question(self):
        res = self.client().post('/questions', json={'search': 'Which'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_found']>0)

    def test_search_question_without_result(self):
        res = self.client().post('/questions', json={'search': 'bababensfe'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertFalse(data['questions'])
        self.assertEqual(data['total_found'], 0)

    def test_delete_question(self):
        query = Question.query.filter(Question.question==self.new_question['question']).one_or_none()
        question_id = query.id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

        

    """ def test_422_create_new_question_fail(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'unprocessable') """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()