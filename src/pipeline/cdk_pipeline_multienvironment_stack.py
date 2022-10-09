from aws_cdk import (
    # Duration,
    Stack,
    pipelines,
    aws_codecommit as codecommit,
    Environment,
    CfnOutput

)
from constructs import Construct
from .stages.deploy_app_stage import PipelineStageDeployApp


class CdkPipelineMultienvironmentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 dev_env=Environment,
                 stg_env=Environment,
                 props: dict = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        # Create repository

        rep = codecommit.Repository(
            self,
            props["repository_properties"]["repository_name"],
            repository_name=props["repository_properties"]["repository_name"],
            description=props["repository_properties"]["description"],

        )

        # Create pipeline source based on codecommit repository
        source = pipelines.CodePipelineSource.code_commit(
            repository=rep,
            branch=props["repository_properties"]["branch"]
        )

        # Create pipeline
        pipeline = pipelines.CodePipeline(
            self,
            f"Pipeline{props['project_name']}",
            cross_account_keys=True,
            pipeline_name=f"Pipeline{props['project_name']}",
            synth=pipelines.ShellStep("Synth",
                                      input=source,
                                      commands=[
                                          "npm install -g aws-cdk",
                                          "pip install -r requirements.txt",
                                          "npx cdk synth"
                                      ]
                                      ),
            self_mutation=True,

        )
        # Modify properties, bucket name
        props["storage_resources"]["s3"][0]["environment"]='dev'

        # Create stages
        deploy_dev = PipelineStageDeployApp(self, "DeployDev",
                                            props=props["storage_resources"]["s3"][0], env=dev_env)
        # Add Stage
        deploy_dev_stg= pipeline.add_stage(deploy_dev)

        # Add manual approval to promote staging
        manual_approval = pipelines.ManualApprovalStep("PromoteToStg", comment="Promote to Staging Gate")
        # Define Dependency
        deploy_dev_stg.add_post(manual_approval)


        # Create Stage for Staging Environment
        # Modify properties, bucket name
        props["storage_resources"]["s3"][0]["environment"] = 'stg'

        # Create stages
        deploy_stg = PipelineStageDeployApp(self, "DeployStg", props=props["storage_resources"]["s3"][0], env=stg_env)
        # Add Stage
        pipeline.add_stage(deploy_stg)

        # Build Pipeline
        pipeline.build_pipeline()

        # Define Outputs
        CfnOutput(self, "GRCRepoUrl", value=rep.repository_clone_url_grc, description="GRC Repository Url")
        CfnOutput(self, "PipelineArn", value=pipeline.pipeline.pipeline_arn, description="Pipeline ARN")
        CfnOutput(self, "StageDev", value=deploy_dev.stage_name, description="Stage Dev Name")
