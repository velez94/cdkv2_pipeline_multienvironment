from aws_cdk import (
    aws_iam as iam,
    Aws, aws_lambda as _lambda,
    Duration
)
import os
from constructs import Construct


class LambdaManualApprove(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 project_name: str = None,
                 emails: list = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        dirname = os.path.dirname(__file__)
        self.function = _lambda.Function(self, f'ManualApprovalNotification{project_name}',
                                         runtime=_lambda.Runtime.PYTHON_3_8,
                                         # code=_lambda.Code.asset('CodeCommit_Stack/lambda'),
                                         code=_lambda.Code.from_asset(path=os.path.join(dirname, "lambda/function")),
                                         handler='app.lambda_handler',
                                         function_name=f'ManualApproval_{project_name}',
                                         timeout=Duration.seconds(70),
                                         environment={
                                             "webhook_secret_name": f"webhook_{project_name}_channel"
                                         }
                                         )

        st = iam.PolicyStatement(actions=["secretsmanager:GetSecretValue"],
                                 effect=iam.Effect.ALLOW,
                                 resources=[
                                     f"arn:aws:secretsmanager:{Aws.REGION}:{Aws.ACCOUNT_ID}:secret:webhook_{project_name}_channel-??????"]
                                 )
        self.function.add_to_role_policy(st)

