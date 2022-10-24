from constructs import Construct
from aws_cdk import (
    Stage,
    # Import Aspects
    Aspects
)
# Add AWS Checks
from cdk_nag import AwsSolutionsChecks, NagSuppressions

from ...stacks.simple_s3_stack import SimpleS3Stack


class PipelineStageDeployApp(Stage):

    def __init__(self, scope: Construct, id: str, props: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        stack = SimpleS3Stack(
            self,
            "SimpleS3Stack",
            props=props,

        )
        # Add aspects
        Aspects.of(stack).add(AwsSolutionsChecks(verbose=True))
        # Add Suppression
        NagSuppressions.add_stack_suppressions(stack=stack, suppressions=[
            {"id": "AwsSolutions-S1", "reason": "Demo Purpose"}
        ])
        # set_tags(stack, tags=props["tags"])
