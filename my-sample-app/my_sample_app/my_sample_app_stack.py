from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class MySampleAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # We will define a VPC, then 2 AZs, and then the respective public and private subnets within
        # See this reference page:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/CfnVPC.html

        
        my_vpc = ec2.CfnVPC(
                self,
                "MyVpc",
                cidr_block="10.0.0.0/16",
                enable_dns_hostnames=True,
                enable_dns_support=True,
        )

        my_internet_gateway = ec2.CfnInternetGateway(
            self,
            "MyInternetGateway"
        )
        
        # Attach the gateway to the VPC
        # See the documentation at https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ec2/CfnVPC.html#aws_cdk.aws_ec2.CfnVPC.attr_vpc_id
        ec2.CfnVPCGatewayAttachment(self, "MyVpcGatewayAttachment",
            vpc_id=my_vpc.attr_vpc_id,
            internet_gateway_id=my_internet_gateway.attr_internet_gateway_id,
            )

        # Let's add a public and private subnet, plus some route tables to each of the availability zones.
        # I also need a subnet-route table association.
        # For the public route, we'll use CfnRoute
        
        my_subnets = [
            {'cidr_block' : '10.0.0.0/24','public' : True},
            {'cidr_block' : '10.0.1.0/24','public' : True},
            {'cidr_block' : '10.0.2.0/24','public' : False},
            {'cidr_block' : '10.0.3.0/24','public' : False},
        ]
        
        # The availability_zones.fget statement is new to me.  It makes sense we would be able to query CF for the availability zones,
        # and upon seeing the code it now makes sense they would come back as a list.  For this information, I would have had to rely
        # on somebody else or a working example to show me the way.
        for i,subnet in enumerate(my_subnets):
            subnet_resource = ec2.CfnSubnet(
                self,
                f'subnet{i+1}',
                vpc_id=my_vpc.attr_vpc_id,
                cidr_block=subnet['cidr_block'],
                map_public_ip_on_launch=subnet['public'],
                availability_zone=Stack.availability_zones.fget(self)[i%2]
            )
            
            # Here, I am creating a route table for each subnet into the VPC.
            route_table = ec2.CfnRouteTable(self,
                                            f'Subnet{i+1}RouteTable',
                                            vpc_id=my_vpc.attr_vpc_id)
            
            # I can see now that I have to create one association for each route-table to subnet, one a one-to-one basis.
            # The lesson learned for me is that defining a route table does nothing without specifying to which subnet it is
            # associated.  At this point, I would need this is how an AWS VPC/subnet/route table network has to work.
            # In my previous exercises, I did not have to get into this type of detail, so I learned something new.
            ec2.CfnSubnetRouteTableAssociation(self,
                                            f'Subnet{i+1}RouteTableAssociation',
                                            route_table_id=route_table.attr_route_table_id,
                                            subnet_id=subnet_resource.attr_subnet_id)
            # Now let's get our routes
            # I can now deduce that we are only routing subnets identified as public to the internet gateway from before.
            # This is the route from a specific route table to the internet gateway.
            if subnet['public']:
                ec2.CfnRoute(self,
                            f'Subnet{i+1}PublicRoute',
                            route_table_id=route_table.attr_route_table_id,
                            destination_cidr_block='0.0.0.0/0',
                            gateway_id=my_internet_gateway.attr_internet_gateway_id)
