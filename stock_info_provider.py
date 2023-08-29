import json
import random
import boto3
import os

stock_available = ['ADBL','CZBIL','EBL','GBIME','HBL', 'KBL','MBL','NABIL','NBL','NCCB','PCBL','PRVU','SBI','SCB','SRBL','STC','API','UIC','LIC','NLIC']
stock_current_price_dict = {}

def load_stock():
    buy_random = random.randint(0, len(stock_available)-1)
    sell_random = random.randint(0, len(stock_available)-1)
    while(buy_random == sell_random):
        sell_random = random.randint(0, len(stock_available)-1)
        
    for stock in stock_available:
        random_number = random.randint(150, 650)
        stock_current_price_dict[stock] = random_number

    stock_current_price_dict[stock_available[buy_random]] = random.randint(101, 149)
    stock_current_price_dict[stock_available[sell_random]] = random.randint(651, 800)

sqs = boto3.client('sqs')
def lambda_handler(event, context):
    try:
        load_stock()
        # Send the event payload to an SQS queue
        queue_url = os.environ['SQS_QUEUE_URL']
        for stock, price in stock_current_price_dict.items():
            a = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps({stock: price}))

        print("Event payload sent to SQS")

        return {
            'statusCode': 200,
            'body': 'Event processed and sent to SQS'
        }
    except Exception as e:
        print("Error processing messages:", e)
        return {
            'statusCode': 500,
            'body': 'Error processing event: ' + str(e)
        }
