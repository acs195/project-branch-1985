#!/bin/sh
# First deploy of the branch api:
#  - Create cf stack with bucket, role and DB. 
#  - Create the API package using zappa.
#  - Upload the API package to the bucket.
#  - Create cf stack with HTTP API and lambda function.

set -e

PROJECT_NAME=branch-project-1985
S3_BUCKET=branch-project-1985-storage
ZIP_FILENAME=branch-project-1985-api.zip

aws cloudformation create-stack \
    --stack-name BranchProject1985StackBase \
    --template-body file://deploy/cf_template_base.yaml \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --tags Key=NameTag,Value=$PROJECT_NAME

aws cloudformation wait stack-create-complete --stack-name BranchProject1985StackBase


zappa package branch -o /tmp/$ZIP_FILENAME
aws s3 cp \
    /tmp/$ZIP_FILENAME \
    s3://$S3_BUCKET/$ZIP_FILENAME

aws cloudformation create-stack \
    --stack-name BranchProject1985StackApi \
    --template-body file://deploy/cf_template_api.yaml \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --tags Key=NameTag,Value=$PROJECT_NAME

aws cloudformation wait stack-create-complete --stack-name BranchProject1985StackApi

exit 0
