from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MyL2SampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_vpc = ec2.Vpc(
            scope=self,
            id="MyVPC",
            nat_gateways=0,
        )