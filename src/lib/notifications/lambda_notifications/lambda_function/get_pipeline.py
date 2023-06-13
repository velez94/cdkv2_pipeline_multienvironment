import boto3


def get_pipeline_status(pipeline_name: str = None):
    client = boto3.client('codepipeline')
    response = client.get_pipeline_state(
        name=pipeline_name
    )
    return response


def get_token(status: dict = None, stage_name: str = None, action_name: str = None):
    stages = status['stageStates']
    token = None
    for s in stages:
        if s['stageName'] == stage_name:
            for st in s['actionStates']:
                if st['actionName'] == action_name:
                    token = st['latestExecution']['token']
    return token
