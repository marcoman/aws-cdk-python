from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)
from constructs import Construct

class MyL2SampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Per the documentation at https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html

        # A default VPC configuration will create public and private subnets. However, if natGateways:0 and 
        # subnetConfiguration is undefined, default VPC configuration will create public and isolated subnets.
        # See Advanced Subnet Configuration below for information on how to change the default subnet configuration.

        # We also use nat_gateways = 0 to save money.
        my_vpc = ec2.Vpc(
            scope=self,
            id="MyVPC",
            nat_gateways=0,
        )

        # next, let's 

        # Let's create a webserver using the above.
        web_server = ec2.Instance(
            scope=self,
            id="WebServer",
            machine_image = ec2.MachineImage.latest_amazon_linux2(),
            instance_type = ec2.InstanceType.of(
                instance_class=ec2.InstanceClass.T2,
                instance_size=ec2.InstanceSize.MICRO),
                vpc = my_vpc,
                vpc_subnets = ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                user_data_causes_replacement=True
        )

        # Now let's attach an elastic IP to our isntance to persist the name when we update
        ec2.CfnEIP(scope = self,
                   instance_id = web_server.instance_id,
                   id = "MyEIP")
        
        # Next, install nginx
        web_server.add_user_data('yum update -y',
                                 'amazon-linux-extras install nginx1',
                                 'service nginx start'
                                 )

        CfnOutput(self, 'WebServerDnsName',
                  value=web_server.instance_public_dns_name
                  )


