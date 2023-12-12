from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# SQLite database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sat_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SATResult(db.Model):
    __tablename__ = 'sat_results'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
    pincode = db.Column(db.String(255))
    sat_score = db.Column(db.Integer)
    passed = db.Column(db.String(255))

# Function to calculate "Passed" based on SAT score
def calculate_passed(score):
    return "Pass" if score > 30 else "Fail"

@app.route('/scores', methods=['POST'])
def insert_data():
    data = request.get_json()

    name = data['name']
    address = data['address']
    city = data['city']
    country = data['country']
    pincode = data['pincode']
    sat_score = data['sat_score']

    
    # Calculate Passed field
    passed = calculate_passed(sat_score)

    # Add data to the database
    new_result = SATResult(
        name=name,
        address=address,
        city=city,
        country=country,
        pincode=pincode,
        sat_score=sat_score,
        passed=passed
    )

    try:
        db.session.add(new_result)
        db.session.commit()
        return jsonify({'message': 'Data inserted successfully'})
       
    except IntegrityError:
         return jsonify({'message': 'Duplicate entry. Candidate with the same name already exists.'}), 400
   

@app.route('/scores', methods=['GET'])
def view_all_data():
    all_results = SATResult.query.all()
    result = [{'name': result.name, 'address': result.address, 'city': result.city,
               'country': result.country, 'pincode': result.pincode, 'sat_score': result.sat_score,
               'passed': result.passed} for result in all_results]

    return jsonify(result)


@app.route('/rank/<name>', methods=['GET'])
def get_rank(name):

    all_results = SATResult.query.order_by(SATResult.sat_score.desc()).all()

    for i, result in enumerate(all_results, start=1):
        if result.name == name:
            return jsonify({'rank': i})

    return jsonify({'message': 'Candidate not found'}), 404


#Update the SAT Scores
@app.route('/scores/<name>', methods=['PUT'])
def update_score(name):
    data = request.get_json()

    result = SATResult.query.filter_by(name=name).first()

    if result:
        result.sat_score = data['sat_score']
        result.passed = calculate_passed(data['sat_score'])

        db.session.commit()

        return jsonify({'message': 'SAT score updated successfully'})
    else:
        return jsonify({'message': 'Candidate not found'}), 404
    

#Delete the score of candidate
@app.route('/scores/<name>', methods=['DELETE'])
def delete_record(name):
    result = SATResult.query.filter_by(name=name).first()

    if result:
        db.session.delete(result)
        db.session.commit()

        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'message': 'Candidate not found'}), 404

if __name__ == '__main__':
    with app.app_context():      
        db.create_all()
    app.run(debug=True)
