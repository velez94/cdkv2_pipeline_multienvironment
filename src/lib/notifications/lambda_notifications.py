from aws_cdk import (
    SecretValue,
    aws_secretsmanager as secretsmanager,
    aws_lambda as _lambda,
    aws_codedeploy as codedeploy,
    aws_codepipeline as pipeline,
    aws_events as events,
    aws_events_targets as targets,
    Duration
)
import os
from constructs import Construct


class LambdaNotification(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 props: dict = None,
                 pipeline: pipeline.IPipeline = None,
                 emails: list = None,

                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dirname = os.path.dirname(__file__)

        # lambda definitions for events
        lambda_notification = _lambda.Function(self, f"lambdanotification_{props['project_name']}",
                                               runtime=_lambda.Runtime.PYTHON_3_9,
                                               code=_lambda.Code.from_asset(
                                                   os.path.join(dirname, "lambda_notifications/lambda_function")),
                                               handler='app.lambda_handler',
                                               function_name=f"lambdanotification_{props['project_name']}",
                                               timeout=Duration.seconds(70),
                                               environment={
                                                   "webhook_secret_name": f"webhook_{props['project_name']}_channel"
                                               }
                                               )

        secret = secretsmanager.Secret(self, f"webhook_{props['project_name']}_channel",
                                       description="WebHook Url for notifications channel in microsoft teams",
                                       secret_name=f"webhook_{props['project_name']}_channel",
                                       secret_string_value=SecretValue.unsafe_plain_text(props["webhook_ops_channel"])
                                       )
        secret.grant_read(lambda_notification)
        alias = _lambda.Alias(self, f"{props['project_name']}-LambdaAlias",
                              alias_name="Prod_2", version=lambda_notification.current_version)

        codedeploy.LambdaDeploymentGroup(self, f"{props['project_name']}-lambda-DeploymentGroup",
                                         alias=alias,
                                         deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE
                                         )
        pipe_states = pipeline.on_event(id=f"{props['project_name']}-pipelinevent",
                                        description="Event for activate lambda when app_pipeline",
                                        event_pattern=events.EventPattern(
                                            detail={
                                                "state": [
                                                    "SUCCEEDED",
                                                    "INPROGRESS",
                                                    "FAILED",
                                                    "SUPERSEDED",
                                                    "STOPPED",
                                                    "STOPPING",
                                                    "CANCELED",
                                                    "STARTED",
                                                    "RESUMED",
                                                    "ABANDONED"

                                                ]
                                            }
                                        )
                                        )

        # Add subscription event lambda
        # ccomit_detect_changes.add_target(targets.LambdaFunction(lambda_notification_ci))

        pipe_states.add_target(targets.LambdaFunction(lambda_notification))
