::
aws cloudformation package --template-file template.yml --s3-bucket stockbuckluck --output-template-file ./out.yml --profile cloudguru
aws cloudformation deploy --template-file out.yml --stack-name workshop --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --profile cloudguru --region us-east-1
pause