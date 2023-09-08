import os
import boto3

client = boto3.client('ses')


def check_buy_sell_header(statement):
    # Convert the statement to lowercase for case-insensitive matching
    statement = statement.lower()

    if 'sold' in statement:
        return 'sell'
    elif 'bought' in statement:
        return 'buy'
    else:
        return 'unknown'

def lambda_handler(event, context):
    recipient_email_address = os.environ['RECIPIENT_EMAIL_ADDRESS']
    buy_sell_header = check_buy_sell_header(event['body'])
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
            'Data': f"Stock {buy_sell_header} Info",
        },
    },
    Source=recipient_email_address
    )
    
    return {
        'statusCode': 200,
        'body': "Email Sent Successfully. MessageId is: " + response['MessageId']
    }