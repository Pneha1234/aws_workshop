import os

def lambda_handler(event, context):
    try:
        stock_live_details = event
        print("Input data from Step Functions:", stock_live_details)
        recommendation = generate_stock_recommendation(stock_live_details)
        return {
            'statusCode': 200,
            'body': recommendation
        }
    except Exception as e:
        error_message = {
            'status': 'error',
            'message': 'Error processing input: ' + str(e)
        }
        return {
            'statusCode': 500,
            'body': error_message
        }


def generate_stock_recommendation(stock_portfolio_list, stock_live_details):
    # suggested_code
    # current_stock_name, current_stock_price = next(iter(stock_live_details.items()))
    current_stock_name = next(iter(stock_live_details))
    current_stock_price = stock_live_details[current_stock_name]
    if current_stock_price > 650:
        return ({"status":"sell", "stock_name":current_stock_name, "rate": current_stock_price})
    elif current_stock_price < 150:
        return ({"status":"buy", "stock_name":current_stock_name, "rate": current_stock_price})
    else:
        return ({"status":"hold", "stock_name":current_stock_name, "rate": current_stock_price})
