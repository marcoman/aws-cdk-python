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
from aws_solutions_constructs.aws_lambda_dynamodb import (
    LambdaToDynamoDB,
)

class ServerlessAppL3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        products_backend = LambdaToDynamoDB(self, "ProductsBackend",
                                            lambda_function_props = lambda_.FunctionProps(
                                                code=lambda_.Code.from_asset("lambda_src"),
                                                handler="product_list_function.lambda_handler",
                                                runtime=lambda_.Runtime.PYTHON_3_12,
                                                ),
                                            table_environment_variable_name="TABLE_NAME",
                                            table_permissions='Read')
        
        products_table = products_backend.dynamo_table
        products_table.apply_removal_policy(RemovalPolicy.DESTROY)
        
        product_list_function = products_backend.lambda_function
        product_list_url = product_list_function.add_function_url(auth_type=lambda_.FunctionUrlAuthType.NONE)
        
        CfnOutput(self,
            "ProductListUrl",
            value = product_list_url.url,
            description="This is our URL to our Lambda"
            )

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


