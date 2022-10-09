import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_pipeline_multienvironment.cdk_pipeline_multienvironment_stack import CdkPipelineMultienvironmentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in src/cdk_pipeline_multienvironment_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkPipelineMultienvironmentStack(app, "cdk-pipeline-multienvironment")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
