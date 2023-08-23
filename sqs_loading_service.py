import json
import boto3
import os
from dotenv import load_dotenv


sqs = boto3.client('sqs')
load_dotenv('dev.env')
def lambda_handler(event, context):
    try:
        event_payload = event['route']
        print("Event received from EventBridge:", event_payload)

        # Send the event payload to an SQS queue
        queue_url = os.environ['SQS_QUEUE_URL']
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event_payload))
        print("Event payload sent to SQS")

        return {
            'statusCode': 200,
            'body': json.dumps('Event processed and sent to SQS')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event: ' + str(e))
        }
