import boto3
import os

stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            # Process SQS message
            stock_detail = record['body']
            print("Message received from SQS:", stock_detail)

            # Trigger Step Function with the message data as input
            state_machine_arn = os.environ['STATE_MACHINE_ARN']
            response = stepfunctions.start_execution(
                stateMachineArn=state_machine_arn,
                input=stock_detail
            )

            print("Step Function execution triggered:", response)

        return {
            'statusCode': 200,
            'body': 'Messages processed and Step Function triggered'
        }
    except Exception as e:
        print("Error processing messages:", e)
        return {
            'statusCode': 500,
            'body': 'Error processing messages: ' + str(e)
        }
