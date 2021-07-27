import json
import boto3
import os

def lambda_handler(event, context):
    dynamodb=boto3.client('dynamodb')
    response=dynamodb.update_item(
        TableName = os.environ['TABLE_NAME'],
        Key={
            'siteUrl':{'S': "ya-resume.com"}
        },
	    UpdateExpression='SET visits = visits + :inc',
	    ExpressionAttributeValues={
	        ':inc': {'N': '1'}
	    },
	    ReturnValues="UPDATED_NEW"
	)
    print response

    # Format dynamodb response into variable count
    responseBody = json.dumps(
        {"count": int(response['Attributes']['visits']['N'])}
    )

    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": responseBody
    }

    return apiResponse