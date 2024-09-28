import aws_cdk as core
import aws_cdk.assertions as assertions

from my_l2_sample_app.my_l2_sample_app_stack import MyL2SampleAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_l2_sample_app/my_l2_sample_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyL2SampleAppStack(app, "my-l2-sample-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
