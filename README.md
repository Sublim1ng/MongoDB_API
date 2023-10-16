# MongoDB_API
## 1. Schema Design <br>
After scanning the five .csv files, I found that they are related by the column "id" or "job_id". I joined them together but found the merged data frame is really messy. In addition, Mongo shell only accepts JSON files. I need to reorganize the data frame. "job_id", "company", "job", and "industry" in the final schema are the four keys I selected. "job_id" directly maps to the column in the data frame, while the other three keys map to nested JSON objects containing more key-value pairs. <br>
## 2. Import Data and Connect API <br>
**Data Import:** <br>
```bash
mongoimport --db mydb --collection data --file /ds5760/mongo/nested_data.json --jsonArray
``` 
**Connect API:** <br>
We have an existing "app" folder and a "run-app.py" file. We just need to run: <br>
```bash
python run-app.py
```
## 3. Flask APP (In Postman, DON'T USE LOCAL HOST)
**Homepage(Method: "GET"):**
```bash
http://127.0.0.1:5000/
```
**Create a Job Post(Method: "POST"):**
```bash
http://127.0.0.1:5000/create/jobPost
```
```bash
Body >> Raw >> JSON
```
```bash
{
  "title": "Software Engineer",
  "description": "Responsible for developing and maintaining software applications.",
  "industry": "Tech",
  "average_salary": "90000",
  "location": "San Francisco, CA"
}
```
**View Job Details(Method: "GET"):**
```bash
http://127.0.0.1:5000/search_by_job_id/1
```
It returns the details of the job that has job_id: 1. <br>

**Update Job Details(Method: "POST":**
```bash
http://127.0.0.1:5000/update_by_job_title
```
```bash
Body >> Raw >> JSON
```
```bash
{
   "title": "Risk Analyst",
   "description": "Calculate potential investment risk for clients",
   "salary": "90000",
   "location": "Iowa City, IA"
}
```

**Remove Job Listing(Method: "DELETE"):**
```bash
http://127.0.0.1:5000/delete_by_job_title
```
```bash
Body >> Raw >> JSON
```
```bash
{
   "title": "IT Consultant",
   "confirm": "yes"
}
```
If you don't enter the "confirm" part, it will return the details of that job. <br>

**Salary Range Query(Method: "GET"):**
```bash
http://127.0.0.1:5000/jobs/salary_range
```
```bash
Params >> Key: min_salary, Value: 60000 >> Key: max_salary, Value: 100000
```

**Job Experience Level Query(Method: "GET"):** <br>
My level definition: <br>
[0,2] >> Entry Level <br>
[3,5] >> Mid Level <br>
[6,100] >> Senior Level <br>
```bash
http://127.0.0.1:5000/jobs/experience_level
```
```bash
Params >> Key: experience_level, Value:Mid Level
```

**Top Companies in an Industry(Method: "GET"):**
```bash
http://127.0.0.1:5000/companies/top_in_industry
```
```bash
Params >> Key: industry, Value: Tech
```

