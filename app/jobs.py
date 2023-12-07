'''Module for serving API requests'''

from app import app
from bson.json_util import dumps, loads
from flask import request, jsonify
import json
import ast # helper library for parsing data from string
from importlib.machinery import SourceFileLoader
from pymongo import MongoClient
from bson.objectid import ObjectId

# 1. connect to the client
client = MongoClient(host="localhost", port=27017)

# Import the utils module
utils = SourceFileLoader('*', './app/utils.py').load_module()

# 2. Select the database
db = client.mydb
# Select the collection
collection = db.data


# route decorator that defines which routes should be navigated to this function
@app.route("/") # '/' for directing all default traffic to this function get_initial_response()
def get_initial_response():

    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to class on MongoDB with Web API'
    }
    resp = jsonify(message)
    # Returning the object
    return resp

@app.route("/create/jobPost", methods=['POST'])
def create_job_post():
    try:
        data = request.get_json()
        
        # Validate data
        if not data.get('title') or not data.get('industry'):
            return jsonify({"error": "Title and industry are required"}), 400
        
        job_id = collection.insert_one(data).inserted_id
        return jsonify({"message": "Job post created", "job_id": str(job_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_by_job_id/<job_id>', methods=['GET'])
def get_by_job_id(job_id):
    try:
        # Query the document
        result = collection.find_one({"job_id": int(job_id)})
        
        # If document not found
        if not result:
            return jsonify({"message": "Job not found"}), 404
        
        # Convert ObjectId to string
        result['_id'] = str(result['_id'])
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/update_by_job_title", methods=['POST'])
def update_by_job_title():
    try:
        data = request.get_json()

        # Retrieve job title and check its existence
        job_title = data.get('title', None)
        if not job_title:
            return jsonify({"error": "Job title is required"}), 400

        # Check if job exists in the collection
        existing_job = collection.find_one({"job.title": job_title})
        if not existing_job:
            return jsonify({"message": "Job with the given title not found"}), 404

        # Prepare update fields for the nested structure
        updates = {}
        for field in ['description', 'average_salary', 'location']:
            if field in data:
                updates[f'job.{field}'] = data[field]

        # Validate the updates
        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        # Update the job in the collection
        collection.update_one({"job.title": job_title}, {"$set": updates})

        return jsonify({"message": "Job details updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_by_job_title', methods=['DELETE'])
def delete_by_job_title():
    data = request.json
    job_title = data.get('title')

    # Validate the job title input
    if not job_title:
        return jsonify({"error": "Job title is required"}), 400

    # Find the job by title
    job_details = collection.find_one({"job.title": job_title})

    # If job not found
    if not job_details:
        return jsonify({"message": "Job not found"}), 404

    # Check if the request contains a confirmation field
    if data.get('confirm') == "yes":
        # Delete the job listing if confirmed
        collection.delete_one({"job.title": job_title})
        return jsonify({"message": f"The job titled '{job_title}' has been deleted."})

    # If not confirmed, return the job details for confirmation
    job_details['_id'] = str(job_details['_id'])  
    return jsonify(job_details)
    
@app.route("/jobs/salary_range", methods=['GET'])
def query_jobs_by_salary():
    # Retrieve query parameters
    min_salary = request.args.get('min_salary', type=int)
    max_salary = request.args.get('max_salary', type=int)
    
    # Validate if both min_salary and max_salary are provided
    if min_salary is None or max_salary is None:
        return jsonify({"error": "Please provide both min_salary and max_salary parameters"}), 400

    # Query the database
    jobs = collection.find({
        "job.average_salary": {"$gte": min_salary, "$lte": max_salary}
    })

    # Convert the results to a list
    result = []
    for job in jobs:
        job["_id"] = str(job["_id"])
        result.append(job)

    return jsonify(result)
    
@app.route("/jobs/experience_level", methods=['GET'])
def query_jobs_by_experience():
    # Retrieve the experience_level query parameter
    experience_level = request.args.get('experience_level')
    
    if experience_level == "Entry Level":
        min_years, max_years = 0, 2
    elif experience_level == "Mid Level":
        min_years, max_years = 3, 5
    elif experience_level == "Senior Level":
        min_years, max_years = 6, 100  
    else:
        return jsonify({"error": "Invalid experience_level provided. Choose from 'Entry Level', 'Mid Level', or 'Senior Level'."}), 400

    # Query the database 
    jobs = collection.find({
        "job.years_of_experience": {"$gte": min_years, "$lte": max_years}
    })

    # Convert results to a list
    result = []
    for job in jobs:
        job["_id"] = str(job["_id"])
        result.append(job)

    return jsonify(result)
    
@app.route('/companies/top_in_industry', methods=['GET'])
def get_top_companies_in_industry():
    industry_name = request.args.get('industry')
    
    # Aggregate data to get top companies based on number of job listings
    pipeline = [
        {
        "$match": {"industry.industry_name": industry_name}
        },
        {
        "$group": {"_id": "$company.name","count": {"$sum": 1}}
        },
        {
        "$sort": {"count": -1}
        }
    ]

    result = list(collection.aggregate(pipeline))
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    '''Send message to the user if route is not defined.'''

    message = {
        "err":
            {
                "msg": "This route is currently not supported."
            }
    }

    resp = jsonify(message)
    # Sending 404 (not found) response
    resp.status_code = 404
    # Returning the object
    return resp


#step 1: create your endpoint name/path + method
#step 2: define your view function for the endpoint
#step 3: do some basic processing/clean up on your user request object
#step 4: do pymongo calls to interact with your mongodb
