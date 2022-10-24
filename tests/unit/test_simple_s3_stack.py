import aws_cdk as core
import aws_cdk.assertions as assertions

from ...src.stacks.simple_s3_stack import SimpleS3Stack
from ...project_configs.helpers.project_configs import props


# example tests. To run these tests, uncomment this file along with the example
# resource in src/stacks/simple_s3_stack.py
def test_s3_bucket_created():
    app = core.App()
    props["storage_resources"]["s3"][0]["environment"] = 'dev'
    stack = SimpleS3Stack(app, "SimpleS3Stack", props=props["storage_resources"]["s3"][0])
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }
    })
