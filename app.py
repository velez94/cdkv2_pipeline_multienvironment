#!/usr/bin/env python3
import os

import aws_cdk as cdk

from src.stacks.simple_s3_stack import SimpleS3Stack
from src.pipeline.cdk_pipeline_multienvironment_stack import CdkPipelineMultienvironmentStack
from project_configs.helpers.project_configs import props, env_client_deployment_account, env_devsecops_account, env_client_stg_account
from project_configs.helpers.helper import set_tags

app = cdk.App()
pipeline_stack = CdkPipelineMultienvironmentStack(
    app,
    "CdkPipelineMultienvironmentStack",
    props=props,
    env=env_devsecops_account,
    dev_env= env_client_deployment_account,
    stg_env=env_client_stg_account
)
set_tags(pipeline_stack, tags=props["tags"])
app.synth()
