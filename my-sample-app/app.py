#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from datetime import datetime

from my_sample_app.my_sample_app_stack import MySampleAppStack

app = cdk.App()
MySampleAppStack(app,
                 "MySampleAppStack",
    )

cdk.Tags.of(app).add("Project", "MySampleApp")
Tags.of(app).add("Owner", "Marco Morales")
Tags.of(app).add("Created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
cdk.Tags.of(app).add("Purpose", "Learning")


app.synth()
