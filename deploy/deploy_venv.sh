#!/bin/sh
# Deploy virtual env as a new version of the Layer in AWS Lambda
set -e

LAYER_NAME=project-branch-layer

# Create virtual env in a temporary folder
virtualenv -p python3.9 /tmp/ztemp_venv

# Install the requirements
/tmp/ztemp_venv/bin/pip install -r requirements.txt

# Compress the virtual env into the project-branch-layer.zip
mkdir -p /tmp/ztemp/python
cp -r /tmp/ztemp_venv/lib/python3.9/site-packages/* /tmp/ztemp/python/
rm -rf /tmp/ztemp/python/boto* /tmp/ztemp/python/pip* /tmp/ztemp/python/setuptools* \
       /tmp/ztemp/python/gunicorn* /tmp/ztemp/python/uvicorn* /tmp/ztemp/python/uvloop*
cd /tmp/ztemp
zip -r ${OLDPWD}/project-branch-layer.zip python
cd ${OLDPWD} && rm -rf /tmp/ztemp && rm -rf /tmp/ztemp_venv

# Upload zip layer to S3
aws s3 cp project-branch-layer.zip s3://project-branch-common && rm project-branch-layer.zip

# Deploy the new version of the layer
aws lambda publish-layer-version \
    --layer-name $LAYER_NAME \
    --content S3Bucket=project-branch-common,S3Key=project-branch-layer.zip \
    --compatible-runtimes python3.9

exit
