from constructs import Construct
from aws_cdk import (
    Stage
)

from ...stacks.simple_s3_stack import SimpleS3Stack


class PipelineStageDeployApp(Stage):

    def __init__(self, scope: Construct, id: str, props: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        stack = SimpleS3Stack(
            self,
            "SimpleS3Stack",
            props=props,

        )
        # set_tags(stack, tags=props["tags"])
