import json


def lambda_handler(event, context):
    print(event)
    portfolio_stock = {"stock_name": "abc",
                       "stock_price": "300"}


    if (event.get('route')):
        print('this is scheduled event')
        
        recommended_stock = (event.get('body'))
        if recommended_stock['stock_name'] == portfolio_stock['stock_name'] and recommended_stock['stock_price'] > \
                portfolio_stock['stock_name']:
            print('buy stock')
        else:
            print('sell stock')


    else:
        print('this is from sqs events')

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
