import json

def lambda_handler(event, context):
    print(event)
    if(event.get('detail-type')):
        print('this is scheduled event')
    else:
        print('this is from api-gateway')
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
