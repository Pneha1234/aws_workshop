import json
import boto3
import os

stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):
    stock_portfolio_str = os.environ['STOCK_PORTFOLIO'] # comma separated stock names from given list: ADBL,EBL,GBIME,HBL,KBL,MBL,NABIL,NBL,NCCB,PCBL,PRVU,SBI,SCB,SRBL,STC,API,UIC,LIC,NLIC
    stock_portfolio_list = stock_portfolio_str.split(',')
    for owned_stock_name in stock_portfolio_list:
        owned_stock_name = owned_stock_name.strip().upper()    

    try:
        for record in event['Records']:
            # Process SQS message
            current_stock_detail = record['body']
            current_stock_name = next(iter(json.loads(current_stock_detail)))
            
            if current_stock_name not in stock_portfolio_list:
                return {
                'statusCode': 200,
                'body': 'stock not owned'
            }

            print("Message received from SQS:", current_stock_detail)

        # Trigger Step Function with the message data as input
        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        response = stepfunctions.start_execution(
            stateMachineArn=state_machine_arn,
            input=current_stock_detail
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
