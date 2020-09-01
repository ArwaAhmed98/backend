
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
        self.database_path = "postgres://{}/{}".format('postgres','123','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #give the attribuites of the class any values
        self.new_Q={ 
            'question' : 'How are you ? ',
            'answer' : 'Fine,Thanks',
          'difficulty': 3,
            'category': '3'}
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    #################################################################
    #############################################################
    def test_get_paginated_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_questions'])
        
    def test_404_sent_requesting_beyond_valid_page(self):
        
        res=self.client().get('/questions?page=1000' , json={'diffculty' :1}) 
        #Check that 404 not found will pop up for a fake data 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success', False])
        self.assertEqual(['message'] , 'resource Not found')
        
    #################################################################
    #############################################################
    def test_delete_book(self):
        res= self.client().delete('/questions/1')
        data=json.loads(res.data)
        x=Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(x,None)
        
    #if we tried to delte a Question with id that does not exist in our database ,  we get formatted error
    def test_404_if_book_doesnot_exist(Self):
        res=self.client().delete('/questions/10000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(['message'] , 'unprocessable')
    
    #################################################################
    #############################################################
    def post_Question():
        
        res=self.client().post('/questions' , json = self.new_Q)
        data=json.loads(res.data)
    
    
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        
    def test_405_for_failed_post(self): #405 =>Method is not allowed
        res=self.client().post('/questions/65' , json = self.new_Q)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'] , 'method not allowed')   
        
        
        
        
        
             
    # """
    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    # """
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()