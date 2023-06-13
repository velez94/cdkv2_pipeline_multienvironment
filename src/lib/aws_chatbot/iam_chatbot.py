from aws_cdk import (
    aws_iam as iam,
    CfnOutput,
)

from constructs import Construct


class IAMAWSChatbot(Construct):

    def __init__(self, scope: Construct, construct_id: str,
                 project_name: str = None,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Define Role with manage policies
        self.chat_role = iam.Role(self, f"AWSChatbotRole-{project_name}",
                                  assumed_by=iam.ServicePrincipal(service="chatbot"),
                                  role_name=f"AWSChatbotRole-{project_name}",
                                  description=f"AWS Chatbot Role for {project_name}",
                                  managed_policies=[
                                      iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name(
                                          "AWSResourceExplorerReadOnlyAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AWSSupportAccess"),
                                      iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipelineApproverAccess"),
                                  ]
                                  )
        # Create custom policies for security
        chat_denny = iam.PolicyStatement(effect=iam.Effect.DENY, actions=["iam:*",
                                                                          "s3:GetBucketPolicy",
                                                                          "ssm:*",
                                                                          "sts:*",
                                                                          "kms:*",
                                                                          "cognito-idp:GetSigningCertificate",
                                                                          "ec2:GetPasswordData",
                                                                          "ecr:GetAuthorizationToken",
                                                                          "gamelift:RequestUploadCredentials",
                                                                          "gamelift:GetInstanceAccess",
                                                                          "lightsail:DownloadDefaultKeyPair",
                                                                          "lightsail:GetInstanceAccessDetails",
                                                                          "lightsail:GetKeyPair",
                                                                          "lightsail:GetKeyPairs",
                                                                          "redshift:GetClusterCredentials",
                                                                          "storagegateway:DescribeChapCredentials"],
                                         resources=["*"]
                                         )

        chat_cw = iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                      actions=["cloudwatch:Describe*",
                                               "cloudwatch:Get*",
                                               "cloudwatch:List*"],
                                      resources=["*"]
                                      )
        policy = iam.Policy(self, f"AWSChatbotCWPolicy-{project_name}",
                            policy_name=f"AWSChatbotCWPolicy-{project_name}",
                            statements=[chat_cw, chat_denny]
                            )
        self.chat_role.attach_inline_policy(policy)

        CfnOutput(self, "AWSChatBotRoleARN", description="AWSChatBotRoleARN", value=self.chat_role.role_arn)
