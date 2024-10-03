#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from datetime import datetime

from serverless_app_l3.serverless_app_l3_stack import ServerlessAppL3Stack

app = cdk.App()
ServerlessAppL3Stack(app, "ServerlessAppL3Stack",
    )

cdk.Tags.of(app).add("Project", "MyServerlessAppL3")
Tags.of(app).add("Owner", "Marco Morales")
Tags.of(app).add("Created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
cdk.Tags.of(app).add("Purpose", "Learning")

app.synth()
