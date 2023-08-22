import json
import boto3

# Initialize the AWS SDK
eventbridge = boto3.client('events')


def lambda_handler(event, context):
    # Parse the incoming event
    try:
        data = json.loads(event['body'])
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input data"})
        }

    # Process data from API Gateway
    api_data = data.get('api_data')
    if api_data:
        print("Received data from API Gateway:", api_data)

    # Process data from EventBridge
    eventbridge_data = data.get('eventbridge_data')
    if eventbridge_data:
        print("Received data from EventBridge:", eventbridge_data)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data received successfully"})
    }
