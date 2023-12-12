import unittest
import json
from appSQL import app, db, SATResult

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():  # Create an application context
            db.create_all()

    def tearDown(self):
        with app.app_context():  # Create an application context
            db.session.remove()
            db.drop_all()

    def test_insert_data(self):
        data = {
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Cityville',
            'country': 'Countryland',
            'pincode': '12345',
            'sat_score': 40
        }

        response = self.app.post('/scores', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Data inserted successfully')

        # Check if the data is inserted in the database
        with app.app_context():  # Create an application context
            result = SATResult.query.filter_by(name='John Doe').first()
            self.assertIsNotNone(result)
            self.assertEqual(result.sat_score, 40)

    def test_insert_data_duplicate_entry(self):
        # Insert a record first
        data = {
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Cityville',
            'country': 'Countryland',
            'pincode': '12345',
            'sat_score': 40
        }
        self.app.post('/scores', data=json.dumps(data), content_type='application/json')

        # Attempt to insert a duplicate record
        response = self.app.post('/scores', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Duplicate entry. Candidate with the same name already exists.')

    # Add more test methods for other endpoints

if __name__ == '__main__':
    unittest.main()
