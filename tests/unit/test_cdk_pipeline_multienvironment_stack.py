import aws_cdk as core
import aws_cdk.assertions as assertions

from ...src.pipeline.cdk_pipeline_multienvironment_stack import \
    CdkPipelineMultienvironmentStack
from ...project_configs.helpers.project_configs import props, env_client_deployment_account, \
    env_devsecops_account, env_client_stg_account


# example tests. To run these tests, uncomment this file along with the example
# resource in src/cdk_pipeline_multienvironment_stack.py
def test_s3_bucket_created():
    app = core.App()
    stack = CdkPipelineMultienvironmentStack(app, "CdkPipelineMultienvironmentStack",
                                             props=props,
                                             env=env_devsecops_account,
                                             dev_env=env_client_deployment_account,
                                             stg_env=env_client_stg_account)
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::CodePipeline::Pipeline", {
        "Stages": [
            {

                "Name": "Source"
            },
            {

                "Name": "Build"
            },
            {

                "Name": "UpdatePipeline"
            },
            {

                "Name": "DeployDev"
            },
            {

                "Name": "DeployStg"
            }
        ]
    })
