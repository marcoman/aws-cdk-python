#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from datetime import datetime

from serverless_app.serverless_app_stack import ServerlessAppStack

app = cdk.App()
ServerlessAppStack(app, "ServerlessAppStack",
    )

cdk.Tags.of(app).add("Project", "MyServerlessApp")
Tags.of(app).add("Owner", "Marco Morales")
Tags.of(app).add("Created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
cdk.Tags.of(app).add("Purpose", "Learning")

app.synth()
