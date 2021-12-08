# project-branch-1985: this is an exercise for branch energy
This API provides the following feature:
- Get information by branch_id
- Insert a new branch_id with its information
- Update the data related to a branch_id

## DB setup
The information is stored in a DynamoDB table

---

## Run app
With Uvicorn:
`uvicorn app.main:app --reload`

With Python:
`python -m app.main`

---

## Test app
`pytest`

---

## Deploy Serverless using Zappa (API Gateway + Lambda)

### AWS Lambda Layer (virtualenv) 
 - Run script deploy/deploy_venv.sh to create a new version of the Layer:
   - `bash deploy/deploy_venv.sh`

- Update zappa settings in zappa_settings.json

- Create new Role with custom policies:
```
aws cloudformation create-stack --stack-name BRANCHAuthStageRoleStack \
--template-body file://.aws/iam.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--tags Key=NameTag,Value=BRANCH
```

- It uses settings from: BRANCH_eat.settings_sls
`zappa deploy [dev | stage | prod]`

- And to update the app:
`zappa update [dev | stage | prod]`

- Add endpoint in AWS to connect the VPC to S3 (or any service required)

In order to use a custom domain with its internal cloudfront:
- First, create an SSL certificate via ACM.
- Then run the following command:
`zappa certify [dev | stage | prod]`

- Run migrations in AWS:
`zappa invoke [dev | stage | prod] db_migrate.upgrade`
