from aws_cdk import (
    # Duration,
    Stack,
    pipelines,
    aws_codecommit as codecommit,
    Environment,
    CfnOutput,
    aws_codebuild as codebuild

)
from constructs import Construct
from .stages.deploy_app_stage import PipelineStageDeployApp
from ..lib.notifications.lambda_notifications import  LambdaNotification

class CdkPipelineMultienvironmentStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 dev_env=Environment,
                 stg_env=Environment,
                 props: dict = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        enable_notifications = props.get("enable_notifications", "false")

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
        # Create unit test step
        unit_test_step = pipelines.CodeBuildStep("UnitTests", project_name="UnitTests",
                                                 commands=[
                                                     "pip install pytest",
                                                     "pip install -r requirements.txt",
                                                     "python3 -m pytest --junitxml=unit_test.xml"
                                                 ],
                                                 partial_build_spec=codebuild.BuildSpec.from_object(
                                                     {"version": '0.2',
                                                      "reports": {
                                                          f"Pytest-{props['project_name']}-Report": {
                                                              "files": [
                                                                  "unit_test.xml"
                                                              ],

                                                              "file-format": "JUNITXML"

                                                          }
                                                      }
                                                      }
                                                 )
                                                 )
        # Create SAST Step for Infrastructure
        sast_test_step = pipelines.CodeBuildStep("SASTTests", project_name="SASTTests",
                                                 commands=[
                                                     "pip install checkov",
                                                     "ls -all",
                                                     "checkov -d . -o junitxml --output-file . --soft-fail"
                                                 ],
                                                 partial_build_spec=codebuild.BuildSpec.from_object(
                                                     {"version": '0.2',
                                                      "reports": {
                                                          f"checkov-{props['project_name']}-Report": {
                                                              "files": [
                                                                  "results_junitxml.xml"
                                                              ],

                                                              "file-format": "JUNITXML"

                                                          }
                                                      }
                                                      }
                                                 ),
                                                 input= pipeline.synth.primary_output


                                                 )

        # Modify properties, bucket name
        props["storage_resources"]["s3"][0]["environment"] = 'dev'

        # Create stages
        deploy_dev = PipelineStageDeployApp(self, "DeployDev",
                                            props=props["storage_resources"]["s3"][0], env=dev_env)

        # Add Stage
        deploy_dev_stg = pipeline.add_stage(deploy_dev)
        # Add Unit test pre step
        deploy_dev_stg.add_pre(unit_test_step)
        # Add SAST step
        deploy_dev_stg.add_pre(sast_test_step)

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
        # Enable notifications
        if enable_notifications == "true":
            LambdaNotification(self, "Notifications", props=props, pipeline=pipeline.pipeline)
        # Define Outputs
        # Define Outputs
        CfnOutput(self, "GRCRepoUrl", value=rep.repository_clone_url_grc, description="GRC Repository Url")
        CfnOutput(self, "PipelineArn", value=pipeline.pipeline.pipeline_arn, description="Pipeline ARN")
        CfnOutput(self, "StageDev", value=deploy_dev.stage_name, description="Stage Dev Name")
