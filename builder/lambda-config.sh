IMAGE_URI=$1
ALIAS_NAME=$2
LAMBDA_CONTAINER_NAME=$3

echo .............................................................
echo updating lambda function with new docker container...
echo .............................................................

# Update the Lambda function with the new Docker image
aws lambda update-function-code --function-name $LAMBDA_CONTAINER_NAME --image-uri $IMAGE_URI

# wait for the lambda function to complete the update before applying any config
aws lambda wait function-updated \
    --function-name $LAMBDA_CONTAINER_NAME

echo .............................................................
echo Creating new version for lambda function...
echo .............................................................

# Publish a new version of the Lambda function
NEW_VERSION=$(aws lambda publish-version --function-name $LAMBDA_CONTAINER_NAME --query 'Version' --output text)
echo "Newest Version:  $NEW_VERSION"


echo .............................................................
echo Updating the Alias with newer version...
echo .............................................................

# Check if the ALIAS_NAME exists
if aws lambda get-alias  --function-name $LAMBDA_CONTAINER_NAME --name $ALIAS_NAME >/dev/null 2>&1; then
    # If the ALIAS_NAME exists, update it with the new version
    aws lambda update-alias  --function-name $LAMBDA_CONTAINER_NAME --name $ALIAS_NAME --function-version $NEW_VERSION
else
    # If the ALIAS_NAME does not exist, create it and point it to the new version
    aws lambda create-alias --function-name $LAMBDA_CONTAINER_NAME --name $ALIAS_NAME --function-version $NEW_VERSION
fi

echo .............................................................

echo "Done!, Lambda function '$LAMBDA_CONTAINER_NAME' updated with Docker image '$IMAGE_URI' and ALIAS_NAME '$ALIAS_NAME' set to version '$NEW_VERSION'"
echo .............................................................