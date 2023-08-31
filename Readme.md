Welcome to the Workshop Code Repository! This repository contains code examples, projects, and resources related to the workshops conducted by Verisk on Architecting Microservices with AWS. Feel free to explore the content and use it to enhance your learning experience.

## Table of Contents

- [Introduction](#introduction)
- [Contents](#contents)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This repository serves as a central hub for code samples and projects covered during this workshops. Even after attending the workshop, you'll find valuable resources to help you understand Architecting Microservices with AWS and implement various concepts effectively.

## Contents

This repository is organized into different sections:

- [Getting Started]((#getting-started))
   - [Cloning the Repository](#cloning-the-repository)
   - [Prerequisites](#prerequisites)
   - [AWS Workshop Overview](#aws-workshop-overview)
   - [AWS Services Used](#aws-services-used)
   - [Workshop Setup](#workshop-setup)
      - [Lambda Layer](#lambda-layer)
      - [SQS](#sqs)
      - [SES](#ses)
      - [Lambda](#lambda)
         - [stock_info_provider](#stock-info-provider)
         - [stock_info_consumer](#stock-info-consumer)
         - [generate_stock_recommendation](#generate-stock-recomendation)
         - [buy_stock](#buy-stock)
         - [sell_stock](#sell-stock)
         - [buy_and_sell_report](#buy-and-sell-report)
      - [Step Function](#step-function)

   
- **/projects**: Hands-on projects and assignments.
- **/resources**: Additional resources, slides, and materials.
- **/solutions**: Solutions to exercises and projects (if applicable).

## Getting Started

Welcome to the AWS Workshop! This guide will walk you through setting up and utilizing the Workshop Code Repository.

### Cloning the Repository

To get started, follow these steps:

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/Pneha1234/workshop_code.git
$ cd workshop_code
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

## Lambda Layer: 
This layer contains third-party dependencies required by the Lambdas.
- Download layer_zip.zip from [here](https://github.com/Pneha1234/worshop_code/blob/master/layer_zip.zip)
- To Create a custom Lambda layer using the layer_zip.zip file with Python 3.11 runtime, use the following steps ,in the AWS Management Console:
  
        * Navigate to the Lambda service.
        * Go to "Layers" in the left menu.
        * Click "Create layer."
        * Provide a name and description for the layer(for this workshop we have named it as layer_zip).
        * Upload the my_layer.zip file.
        * Choose a compatible runtime (Python 3.11 in your case).
        * Click "Create."

## SQS: 
-stock_queue
Create an SQS queue to hold messages and trigger the stock_info_consumer Lambda.

### SES: 
Verify your email identity under SES for sending email reports.
- To Verify an email, use the following steps ,in the AWS Management Console:
   
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
    * Copy the code from stock_info_provider.py and paste into the code console on the new lambda creation page on management   console. 
    * Add the generic layer created above to this lambda.
    * Provide environment variables required i.e. SQS_QUEUE_URL in Environment variables section under Configuration.
    * Goto the permission section and add sqs access to the role.
### stock_info_consumer:
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

## Usage
Feel free to utilize the content in this repository to enhance your understanding of [Topic]. Run code examples, complete projects, and refer to resources to reinforce your learning.

## Contributing
If you'd like to contribute to this repository, follow these steps:

- Fork the repository.
- Create a new branch: git checkout -b feature-name.
- Make your changes and commit them: git commit -m 'Description of changes'.
-  to the branch: git push origin feature-name.
- Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or feedback, don't hesitate to reach out:

- Email: your@email.com
- GitHub: YourUsername
