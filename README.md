# branch-project-1985: this is an exercise for branch energy

This API provides the following features:
- Get information by branch_id
- Insert a new branch_id with its information
- Update the data related to a branch_id

## Swagger docs:
Find it under: url[:port]/docs

## Notes/decisions about the project:
- I chose to write a fully structured api over just functions. Mainly because of order and maintainability. The API may not meet the response times expected because of it.
- I chose non-sql (dynamodb) over sql because of speed, scalability and better handling of additional (unplanned) attributes.
- I chose to use the boto3 dynamodb client over Pynamodb. Even though Pynamodb looks easier to use, I found some limitations and ended up using boto3 because of the fine tune usage it offers.
- The zipped function is almost 50MB. The ideal is to separate the environemt into a lambda layer. That way the zipped function would be really small.
- I know there is a lot of room for improvements. I believe that what I coded should suffice for the purpose of evaluation.
- I'm not confortable with the test strategy here. I should have coded a quick in-memory repository instead of making dependant of an external tool. Also, not happy with the number of test cases.
- The project is not finished. It is still pending to save and query on base on the billing account id.
- This is more or less how I spent my time on this project (approx):
  * 1h: read/understand/extract keypoints to help me design the solution.
  * 2hs: think/evaluate alternative solutions.
  * 1h: prepare scaffolding (taken from another project).
  * 2hs: code one piece of the solution.
  * 3hs: test and debug issues with local dynamodb tool (dynalite).
  * 3hs: more the deployment script and cloudformation template.
  * 2hs: more coding and testing.
  * 1h: cleaning and final notes.
  * 1h: finished some unfinished part of the global secondary index.

## DB setup
The information is stored in a DynamoDB table

---

## Virtual env for the app:
Create a un virtual env:
`python -m venv -p python3.9`

Install the requirements:
`pip install -r requirements_dev.txt`

---

## Run app locally:
With Uvicorn:
`uvicorn app.main:app --reload`

With Python:
`python -m app.main`

---

## Test app
For testing the app, we need to install npm package dynalite
`npm install dynalite`
Run dynalite in port 4567:
`dynalite --port 4567`
Run the test suite:
`pytest`

---

## Mypy annotations check
`sh ./scripts/run_mypy.sh`

---

## Deploy Serverless using Zappa + CloudFormation templates
Script to first deploy api
`sh ./deploy/first_deploy.sh`
