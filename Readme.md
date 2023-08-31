# AWS Workshop

Thorough guide for the workshop.

![](./Images/architecturediagram.png "Workshop AWS architecture diagram")

## Prerequisites to build this solution locally
1.python 3.11 installed in the local machine
2. VS Code/Pycharm

## AWS services used
1. Eventbridge (for triggering the workflow every 5 mins)
2. Lambda (for microservices construction)
3. SQS (for queuing messages and triggering stock_info_consumer lambda)
4. Step Function (for orchestrating microservices into the visual workflow)
5. SES (for sending email report)

1. Lambda Layer:
- generic_layer:
    * This is the layer created for the third party dependencies required by the lambda. 
    * Create a custom lambda layer with upload zip option to upload the layer_zip.zip file with Python 3.11 as runtime selected in the management console. 
2. SQS:
- stock_queue:
    * This is the queue aws service used to hold the messages and trigger the stock_info_consumer lambda below(yet to be created) with it. 
    * Create a SQS queue with default values in sqs section under the management console. 
3. SES:(we are just adding this for email verification as identity)
- ses verify identity: 
    * In management console under SES section, under verified identities, create identity with email and verify by clicking on the link in your email.
4. Lambda:
- stock_info_provider:
    * This is the service responsible for generating live prices and feeding to sqs queue. 
    * Copy the code from stock_info_provider.py and paste into the code console on the new lambda creation page on management   console. 
    * Add the generic layer created above to this lambda.
    * Provide environment variables required i.e. SQS_QUEUE_URL in Environment variables section under Configuration.
    * Goto the permission section and add sqs access to the role.
- stock_info_consumer:
    * This is the service responsible for triggering the step function for individual stock info from sqs(also triggered by sqs).
    * Copy the code from stock_info_consumer.py and paste into the code console on the new lambda creation page on management   console.
    * Provide environment variables required i.e. STATE_MACHINE_ARN in Environment variables section under Configuration.
    * Add the generic layer created above to this lambda.
    * Goto the permission section and add sqs, stepfunction access to the role.
    * Finally, add the trigger with batch size 1 and the name pointing to above created sqs queue.
- generate_stock_recommendation:
    * This is the service responsible for generating buy, sell or non recommendation from the fed input matching to the ones on the defined portfolio list in the environment variable.
    * Copy the code from generate_stock_recommendation.py and paste into the code console on the new lambda creation page on management console.
    * Provide environment variables required i.e. STOCK_PORTFOLIO with 15-20 values from (ADBL,CZBIL,EBL,GBIME,HBL, KBL,MBL,NABIL,NBL,NCCB,PCBL,PRVU,SBI,SCB,SRBL,STC,API,UIC,LIC,NLIC) in Environment variables section under Configuration.
- buy_stock:
    * This is the service responsible for processing buy of the ones recommended by above recommendation service.
    * Copy the code from buy_stock.py and paste into the code console on the new lambda creation page on management console.
- sell_stock:
    * This is the service responsible for processing sell of the ones recommended by above recommendation service.
    * Copy the code from sell_stock.py and paste into the code console on the new lambda creation page on management console.
- buy_and_sell_report:
    * This is the service responsible for reporting the user by email for either of buy or sell report.
    * Copy the code from buy_and_sell_report.py and paste into the code console on the new lambda creation page on management console.
    * Provide environment variables required i.e. RECIPIENT_EMAIL_ADDRESS with the verified email above under SES section in Environment variables section under Configuration.
    * Add the generic layer created above to this lambda.
    * Goto the permission section and add ses access to the role.

5. Step Function:
- stock_state_machine:
    * First lets add all the states as in the figure: Add lambda invocation state, add choice state under this, add lambda invocation under rule1, add another lambda invocation under default, then add another lambda invocation under one of the lambda then a succeed section under that lambda.
    * This is the step function that is responsible for orchestration the above created lambdas into a functioning workflow.
    * Under start in workflow studio add lambda invocation state and on the right side under State name add : Generate stock recommendation, Leave integration type as it is, under function name select enter function name and select the generate_stock_recommendation lambda as the lambda, under Payload select use state input as payload, then go to the output tab by scrolling above, then select Filter output with OutputPath and add $.Payload.body in the text box.
    * Now Under Flow tab in the upper left side navigation section add a choice state under the generate stock recommendation state,
    now on the configuration section add.
    * Under start in workflow studio add lambda invocation state and on the right side under State name add : Generate stock recommendation, Leave integration type as it is, under function name select enter function name and select the generate_stock_recommendation lambda as the lambda.


