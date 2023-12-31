Welcome to the Workshop Code Repository! This repository contains code examples, projects, and resources related to the workshops conducted by Verisk Nepal on Architecting Microservices with AWS. Feel free to explore the content and use it to enhance your learning experience.

## Table of Contents

- [Introduction](#introduction)
- [Contents](#contents)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

This repository serves as a central hub for code samples and projects covered during this workshop. Even after attending the workshop, you'll find valuable resources to help you understand Architecting Microservices with AWS and implement various concepts effectively.

## Contents

This repository is organized into different sections:
<a name="top"></a>
- [Getting Started]((#getting-started))
   - [Cloning the Repository](#cloning-the-repository)
   - [Prerequisites](#prerequisites)
   - [AWS Workshop Overview](#aws-workshop-overview)
   - [AWS Services Used](#aws-services-used)
   - [Workshop Setup](#workshop-setup)
      - [SQS](#sqs)
      - [SES](#ses)
      - [Lambda](#lambda)
         - [stock_info_provider](#stock_info_provider)
         - [stock_info_consumer](#stock_info_consumer)
         - [generate_stock_recommendation](#generate_stock_recommendation)
         - [buy_stock](#buy_stock)
         - [sell_stock](#sell_stock)
         - [buy_and_sell_report](#buy_and_sell_report)
      - [Step Function](#step-function)


- [Additional Resources](#additional-resources)


## Getting Started

This guide will walk you through setting up and utilizing the Workshop Code Repository.

### Cloning the Repository

To get started, follow these steps:

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/Pneha1234/aws_workshop.git
$ cd aws_workshop
```

### Prerequisites
Before building and running this solution locally, ensure you have the following prerequisites:

- Python 3.11 installed on your local machine.
- An integrated development environment (IDE) such as Visual Studio Code or PyCharm.

### AWS Workshop Overview
This repository serves as a comprehensive guide to our AWS Workshop. It covers a variety of AWS services and concepts to help you gain a deeper understanding of cloud computing.

![](https://github.com/Pneha1234/worshop_code/blob/master/images/workshop.png)

### AWS Services Used
Throughout the workshop, we'll be leveraging the following AWS services:

- EventBridge: Used for triggering the workflow every 5 minutes.
- Lambda: Employed for constructing microservices.
- SQS: Utilized for queuing messages and triggering the stock_info_consumer Lambda.
- Step Function: Orchestrating microservices into a visual workflow.
- SES: Sending email reports.

## Workshop Setup
To set up the workshop environment, we'll configure various AWS services as follows:

## SQS: 
-stock_queue

Create an SQS queue to hold messages and trigger the stock_info_consumer Lambda.

      * Goto Amazon SQS.
      * Under 'Get Started', click 'Create queue'.
      * Under 'Details', give a 'Name'.
      * Keep all the 'Configuration' default for this demonstration.
      * Click on 'Create queue' at the bottom of the page.
      * SQS is created!

### SES: 
Verify your email identity under SES for sending email reports.
- To Verify an email, use the following steps, in the AWS Management Console:
   
      * Navigate to SES in the dashboard.
      * Click "Email Addresses" on the left.
      * Click "Verify a New Email Address."
      * Enter the email address you want to verify.
      * Click "Verify This Email Address."
      * Open the verification email sent to that address.
      * Click the verification link in the email.
      * Verification is complete!
  
## Lambda:
### stock_info_provider:
    * This is the service responsible for generating live prices and feeding to sqs queue. 
    * Provide environment variables required i.e. SQS_QUEUE_URL in Environment variables section under Configuration.
    * Goto the permission section and add sqs access policy to the role:
    {"Effect": "Allow","Action": ["sqs:SendMessage"],"Resource": "<SQS_ARN>"}
    * Note that we are trying to follow The principle of least privilege (PoLP) as best practice.
     
   - Please copy the code from the following snippet
 ```python
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
```
[Back to Top](#top)
### stock_info_consumer:
    * This is the service responsible for triggering the step function for individual stock info from sqs(also triggered by sqs).
    * Copy the code from stock_info_consumer.py and paste into the code console on the new lambda creation page on management   console.
    * Provide environment variables required i.e. STATE_MACHINE_ARN and STOCK_PORTFOLIO with comma separated values 
    without bracket (ADBL,EBL,GBIME,HBL,KBL,MBL,NABIL,NBL,NCCB,PCBL,PRVU,SBI,SCB,SRBL,STC,API,UIC,LIC,NLIC) in Environment variables section under Configuration.
    * Goto the permission section and add sqs, stepfunction access to the role:
    { "Effect": "Allow", "Action": [ "sqs:ReceiveMessage","sqs:DeleteMessage","sqs:GetQueueAttributes" ], "Resource": "<SQS_ARN>" }
    * Finally, add the trigger with batch size 1 and the name pointing to above created sqs queue.
   - Please copy the code from the following snippet
```python
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
```
- [Back to Top](#top)
### generate_stock_recommendation:
    * This is the service responsible for generating buy, sell or non recommendation from the fed input 
    * matching to the ones on the defined portfolio list in the environment variable.
     * Goto the permission section and add aws lambda basic execution role access
     to the role. i.e   AWSLambdaBasicExecutionRole
   
- Please copy the code from the below snippet
```python
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


def generate_stock_recommendation(stock_live_details):
    current_stock_name = next(iter(stock_live_details))
    current_stock_price = stock_live_details[current_stock_name]

    if current_stock_price > 650:
        return ({"status":"sell", "stock_name":current_stock_name, "rate": current_stock_price})
    elif current_stock_price < 150:
        return ({"status":"buy", "stock_name":current_stock_name, "rate": current_stock_price})
    else:
        return ({"status":"hold", "stock_name":current_stock_name, "rate": current_stock_price})
        
```

- test event:
     * {"PRVU": 295}
- [Back to Top](#top)
### buy_stock:
    * This is the service responsible for processing buy of the ones recommended by above recommendation service.
   - Please use the below code snippet
```python
def lambda_handler(event, context):
    try:
        default_stock_quantity = 50
        stock_name = event['stock_name']
        rate = event['rate']

        # buy and process the stock (simulating buying)
        return {
            'statusCode': 200,
            'body': f'{default_stock_quantity} stocks for {stock_name} bought at {rate} rate for total amount {rate * default_stock_quantity}.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error processing buy: ' + str(e)
        }
```
### sell_stock:
    * This is the service responsible for processing sell of the ones recommended by above recommendation service.
```python
def lambda_handler(event, context):
    try:
        default_stock_quantity = 50
        stock_name = event['stock_name']
        rate = event['rate']

        # sell and process the stock (simulating selling)
        return {
            'statusCode': 200,
            'body': f'{default_stock_quantity} stocks for {stock_name} sold at {rate} rate for total amount {rate * default_stock_quantity}.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error processing buy: ' + str(e)
        }
```
[Back to Top](#top)
### buy_and_sell_report:
    * This is the service responsible for reporting the user by email for either of buy or sell report.
    * Provide environment variables required i.e. RECIPIENT_EMAIL_ADDRESS with the
    verified email above under SES section in Environment variables section under Configuration.
    * Goto the permission section and add ses access to the role. 
    { "Effect": "Allow", "Action": [ "ses:SendEmail" ], "Resource": "<VERIFIED_EMAIL_ARN>" }
```python
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
```
[Back to Top](#top)
### Step Function:
- stock_state_machine:
    * Goto the stock_info_consumer lambda and goto permission section to add state machine execution permission to the role:
    { "Effect": "Allow", "Action": [ "states:StartExecution" ], "Resource": "<STATE_MACHINE_ARN>" }
    * Goto the SES console and under verified identities add your email to the verified identity list where a link is sent to you and should click to verify the email.
    * First let's add all the states as in the figure: Add lambda invocation state, add choice state under this, add lambda invocation under rule1, add another lambda invocation under default, then add another lambda invocation under one of the lambda then a succeed section under that lambda.
    * This is the step function that is responsible for the orchestration of lambdas created above into a functioning workflow.
    * Under start in workflow studio add lambda invocation state and on the right side under State name add: Generate stock recommendation, Leave integration type as it is, under function name, select enter function name and select the generate_stock_recommendation lambda as the lambda, under Payload select use state input as payload, then go to the output tab by scrolling above, then select Filter output with OutputPath and add $.Payload.body in the text box.
    * Now Under Flow tab in the upper left side navigation section add a choice state under the generate stock recommendation state, now on the configuration section add.
    * Under start in workflow studio add lambda invocation state and on the right side under State name add: Generate stock recommendation, Leave integration type as it is, under function name select enter function name and select the generate_stock_recommendation lambda as the lambda.

- [Back to Top](#top)

### Additional Resources
- [AWS Lambda Resources](https://aws.amazon.com/lambda/resources/?aws-lambda-resources-blog.sort-by=item.additionalFields.createdDate&aws-lambda-resources-blog.sort-order=desc)
- [AWS SQS](https://aws.amazon.com/sqs/resources/?amazon-simple-queue-service-sqs-resources-blog.sort-by=item.additionalFields.createdDate&amazon-simple-queue-service-sqs-resources-blog.sort-order=desc)
- [AWS IAM Roles and Policies](https://aws.amazon.com/iam/resources/?iam-blogs.sort-by=item.additionalFields.createdDate&iam-blogs.sort-order=desc)
- [AWS EventBridge](https://aws.amazon.com/eventbridge/resources/)
- [AWS Step Function](https://aws.amazon.com/step-functions/resources/?step-functions.sort-by=item.additionalFields.postDateTime&step-functions.sort-order=desc)


## Usage
Feel free to utilize the content in this repository to enhance your understanding on AWS Services. Run code examples, complete projects, and refer to resources to reinforce your learning.

## Contributing
If you'd like to contribute to this repository, follow these steps:

- Fork the repository.
- Create a new branch: git checkout -b feature-name.
- Make your changes and commit them: git commit -m 'Description of changes'.
-  to the branch: git push origin feature-name.
- Open a pull request.
  
-  [Back to Top](#top)
