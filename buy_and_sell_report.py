import os
import boto3

client = boto3.client('ses')

def lambda_handler(event, context):
    recipient_email_address = os.environ['RECIPIENT_EMAIL_ADDRESS']
    response = client.send_email(
    Destination={
        'ToAddresses': [f'{recipient_email_address}']
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': f"{event['body']}",
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Stock Buy/Sell Info',
        },
    },
    Source= recipient_email_address
    )
    
    return {
        'statusCode': 200,
        'body': "Email Sent Successfully. MessageId is: " + response['MessageId']
    }