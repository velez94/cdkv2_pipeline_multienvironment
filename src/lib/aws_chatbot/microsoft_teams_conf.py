from aws_cdk import (
    aws_chatbot as chatbot,
    aws_sns as sns,
    CfnOutput, Aws
)

from constructs import Construct
from .iam_chatbot import IAMAWSChatbot


class MicrosoftTeamsChannelConfiguration(Construct):

    def __init__(self, scope: Construct, construct_id: str,

                 props: dict = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Iam Role
        chat_iam = IAMAWSChatbot(self, "IAMRole", project_name=props["project_name"])

        # Create sns topic
        self.sns_topíc = sns.Topic(self, props["project_name"], display_name=f"ChatOps{props['project_name']}",
                              topic_name=f"ChatOps{props['project_name']}")
        self.arn_teams = f"arn:aws:chatbot::{Aws.ACCOUNT_ID}:chat-configuration/microsoft-teams-channel/MicrosoftTeamsChannel-{props['project_name']}"
        # Define properties
        self.teams_conf = chatbot.CfnMicrosoftTeamsChannelConfiguration(self,
                                                                        f"MicrosoftTeamsChannel-{props['project_name']}",
                                                                        configuration_name=f"MicrosoftTeamsChannel-{props['project_name']}",
                                                                        iam_role_arn=chat_iam.chat_role.role_arn,
                                                                        # "teamId",
                                                                        team_id=props["team_id"],
                                                                        # "teamsChannelId"
                                                                        teams_channel_id=props["teams_channel_id"],
                                                                        # "teamsTenantId"
                                                                        teams_tenant_id=props["teams_tenant_id"],

                                                                        # the properties below are optional
                                                                        guardrail_policies=[
                                                                            "arn:aws:iam::aws:policy/AWSCodePipeline_FullAccess",
                                                                            "arn:aws:iam::aws:policy/ReadOnlyAccess"
                                                                        ],
                                                                        logging_level="ERROR",
                                                                        sns_topic_arns=[self.sns_topíc.topic_arn],
                                                                        user_role_required=False
                                                                        )

        CfnOutput(self, "OutputTeams", value=self.teams_conf.attr_arn)
