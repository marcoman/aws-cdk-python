from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MyL2SampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Per the documentation at https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html

        # A default VPC configuration will create public and private subnets. However, if natGateways:0 and subnetConfiguration is undefined, default VPC configuration will create public and isolated subnets. See Advanced Subnet Configuration below for information on how to change the default subnet configuration.
        
        my_vpc = ec2.Vpc(
            scope=self,
            id="MyVPC",
            nat_gateways=0,
        )