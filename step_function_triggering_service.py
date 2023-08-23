import json
import boto3
import os
from dotenv import load_dotenv


sqs = boto3.client('sqs')
stepfunctions = boto3.client('stepfunctions')
load_dotenv('dev.env')


def lambda_handler(event, context):
    try:
        for record in event['Records']:
            # Process SQS message
            message_body = json.loads(record['body'])
            print("Message received from SQS:", message_body)

            # Trigger Step Function with the message data as input
            state_machine_arn = os.environ['STATE_MACHINE_ARN']
            response = stepfunctions.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(message_body)
            )

            print("Step Function execution triggered:", response)

        return {
            'statusCode': 200,
            'body': json.dumps('Messages processed and Step Function triggered')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing messages: ' + str(e))
        }
