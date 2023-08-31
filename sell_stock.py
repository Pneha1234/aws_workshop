def lambda_handler(event, context):
    try:
        default_stock_quantity = 50
        stock_name = event['stock_name']
        rate = event['rate']

        # buy and process the stock (simulating buying)
        return {
            'statusCode': 200,
            'body': f'{default_stock_quantity} stocks for {stock_name} sold at {rate} rate for total amount {rate * default_stock_quantity}.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error processing buy: ' + str(e)
        }
