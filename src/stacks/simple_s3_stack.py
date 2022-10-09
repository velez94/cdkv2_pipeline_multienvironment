from aws_cdk import (
    Stack,
    aws_s3 as s3,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct


class SimpleS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, props: dict = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        bucket = s3.Bucket(self, id=props["bucket_name"],
                           bucket_name=f'{props["bucket_name"]}-{props["environment"]}',
                           versioned=True if props["versioned"] == "enable" else None,
                           enforce_ssl=True,
                           encryption=s3.BucketEncryption.S3_MANAGED,
                           removal_policy= RemovalPolicy.DESTROY
                           )
        # Define outputs
        CfnOutput(self, id="S3ARNOutput", value=bucket.bucket_arn, description="Bucket ARN")
