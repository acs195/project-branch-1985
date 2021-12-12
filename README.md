# project-branch-1985: this is an exercise for branch energy

This API provides the following feature:
- Get information by branch_id
- Insert a new branch_id with its information
- Update the data related to a branch_id

## Notes/decisions about the project:
- I chose to write a fully structured api over something like Chalice or SAM. Mainly because of order and maintainability.
- I chose non-sql (dynamodb) over sql because of speed and better handling of additional (unplanned) attributes.
- 

## DB setup
The information is stored in a DynamoDB table

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
