#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Aspects
# from cdk_nag import AwsSolutionsChecks

from src.pipeline.cdk_pipeline_multienvironment_stack import CdkPipelineMultienvironmentStack
from project_configs.helpers.project_configs import props,  env_devsecops_account
from project_configs.helpers.helper import set_tags

app = cdk.App()
# Add cdk-nag Aws Solutions pack with extra verbose logging enabled
#Aspects.of(app).add(AwsSolutionsChecks(verbose= True) )
pipeline_stack = CdkPipelineMultienvironmentStack(
    app,
    "CdkPipelineMultienvironmentStack",
    stack_name= "CdkPipelineMultienvironmentStack",
    props=props,
    env=env_devsecops_account,
    dev_env= props["environments"]["stg"],
    stg_env=props["environments"]["prod"]
)
set_tags(pipeline_stack, tags=props["tags"])
app.synth()
