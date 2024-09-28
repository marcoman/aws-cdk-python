#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags
from datetime import datetime

from my_l2_sample_app.my_l2_sample_app_stack import MyL2SampleAppStack

app = cdk.App()
MyL2SampleAppStack(app,
                   "MyL2SampleAppStack",
    )

cdk.Tags.of(app).add("Project", "MyL2SampleApp")
Tags.of(app).add("Owner", "Marco Morales")
Tags.of(app).add("Created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
cdk.Tags.of(app).add("Purpose", "Learning")

app.synth()
