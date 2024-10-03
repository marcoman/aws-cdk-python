from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    aws_lambda as lambda_,
    CfnOutput,
    aws_cloudwatch as cloudwatch,
    Duration,
)
from constructs import Construct

class ServerlessAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Define a lambda that gets data from a DynamoDB table. 
        # From our lecture, we wish to set the billing_mode to PAY_PER_REQUEST
        # Also, we want to destroy the DB on remove
        products_table = dynamodb.Table(self,
                                        "ProductsTable",
                                        partition_key=dynamodb.Attribute(
                                            name="id",
                                            type=dynamodb.AttributeType.STRING
                                        ),
                                        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                        removal_policy=RemovalPolicy.DESTROY,
        )
        
        # When we review the documentation starting at this location:        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        # We see we have to provide several parameters:
        # - code is the source code (this is the folder to our code)
        # - handler - The name of our method (this will be "lambda_handler")
        # - runtime - This wil be PYTHON_3_12= <aws_cdk.aws_lambda.Runtime object>
        # - environment - to specify the python TABLE_NAME value.
        product_list_function = lambda_.Function(self,
                                                 "ProductListFunction",
                                                 code=lambda_.Code.from_asset("lambda_src"),
                                                 handler="product_list_function.lambda_handler",
                                                 runtime=lambda_.Runtime.PYTHON_3_12,
                                                 environment={
                                                     "TABLE_NAME": products_table.table_name
                                                 },
        )

        # In order to add premissions to the lambda function, we reference the documentation at this link:
        # https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_dynamodb.Table.html and then
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
        # We'll want to read data.

        # For the purpose of testing our CloudWatch alarm, we will remove permission on our function to read the table.
        products_table.grant_read_data(product_list_function.role)
        
        # Now add a Lamda URL to the Lambda function to execute it from the internet
        # See https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.add_function_url
        # The auth_type options are ...AWS_IAM or NONE.  We'll use NONE to keep things simple for now.
        product_list_url = product_list_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)
        print(f'Your URL is {product_list_url.url}')
        
        # See the documentation at https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/CfnOutput.html 
        # Add a line to make the URL easy to get to
        
        CfnOutput(self,
                  "ProductListUrl",
                  value = product_list_url.url,
                  description="This is our URL to our Lambda"
                  )
        
        
        # Configuring an alarm for the Lambda function errors metric.
        # I am mostly following-along with the narrative by the lecturer.  Individually, the information I heard 
        # makes sense.  However, there are about 8 different pieces of information I have to reconcile into a 
        # story to help me understand the solution for the problem we are trying to solve:
        # How do we send a Lambda error to CloudWatch?
        
        # We know our function is product_list_function, and we get its metric_errors.
        # See https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.metric_errors
        errors_metric = product_list_function.metric_errors(
            label="ProductListFunction Errors",
            # For this exercise, I am setting the duration to 1 minute, and not 5 as suggested.
            period=Duration.minutes(1),
            statistic=cloudwatch.Stats.SUM,
        )

       # See https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html#aws_cdk.aws_cloudwatch.Metric.create_alarm
        errors_metric.create_alarm(self,
                                 "ProductListFunction Alarm",
                                 evaluation_periods=1,
                                 threshold=1,
                                 comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                                 treat_missing_data=cloudwatch.TreatMissingData.IGNORE,
        )
