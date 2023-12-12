from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# SAT Scores database 
database = []

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

    # If user already exists in databse then don't insert
    for candidate in database:
            if candidate['name'] == name:
                return jsonify({'message': 'User Already Exist!'})                

    # Add data to the database
    database.append({
        'name': name,
        'address': address,
        'city': city,
        'country': country,
        'pincode': pincode,
        'sat_score': sat_score,
        'passed': passed
    })

    return jsonify({'message': 'Data inserted successfully'})


@app.route('/scores', methods=['GET'])
def view_all_data():
    return jsonify(database)


@app.route('/rank/<name>', methods=['GET'])
def get_rank(name):

    # sorted by SAT score in descending order
    sorted_database = sorted(database, key=lambda x: x['sat_score'], reverse=True)

    for i, candidate in enumerate(sorted_database, start=1):
        if candidate['name'] == name:
            return jsonify({'rank': i})

    return jsonify({'message': 'Candidate not found'}), 404


@app.route('/scores/<name>', methods=['PUT'])
def update_score(name):
    data = request.get_json()

    # Find the candidate in the database
    for candidate in database:
        if candidate['name'] == name:
            # Update the SAT score
            candidate['sat_score'] = data['sat_score']

            # Recalculate the "Passed" field
            candidate['passed'] = calculate_passed(data['sat_score'])

            return jsonify({'message': 'SAT score updated successfully'})

    return jsonify({'message': 'Candidate not found'}), 404


@app.route('/scores/<name>', methods=['DELETE'])
def delete_record(name):
    # Remove the candidate from the database
    for candidate in database:
        if candidate['name'] == name:
            database.remove(candidate)
            return jsonify({'message': 'Record deleted successfully'})

    return jsonify({'message': 'Candidate not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
