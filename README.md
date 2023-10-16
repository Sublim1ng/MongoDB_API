# MongoDB_API
## 1. Schema Design <br>
After scanning the five .csv files, I found that they are related by the column "id" or "job_id". I joined them together but found the merged data frame is really messy. In addition, Mongo shell only accepts JSON files. I need to reorganize the data frame. "job_id", "company", "job", and "industry" in the final schema are the four keys I selected. "job_id" directly maps to the column in the data frame, while the other three keys map to nested JSON objects containing more key-value pairs. <br>
## 2. Import Data and Connect API <br>
This step is simple: <br>
**Data Import:** <br>
<span style="color:red">mongoimport --db mydb --collection data --file /ds5760/mongo/nested_data.json --jsonArray</span> <br>
**Connect API** <br>
We have an existing "app" folder and a "run-app.py" file. We just need to run: <br>
python run-app.py <br>

