import os
import pymsteams
from get_secret import get_secret
from get_pipeline import get_pipeline_status, get_token
import json


def set_state(message, state, connection_card, activity_text):
    if message['detail']['state'] == 'STARTED':
        state.text(message['detail']['state'])
        state.activityText(activity_text)
        state.activityImage(
            "https://support.content.office.net/en-us/media/6b8c0bff-7ddc-4bff-9101-8360f8c8a727.png")
    elif message['detail']['state'] == 'SUCCEEDED':
        state.activityText(activity_text)
        state.activityImage(
            "https://support.content.office.net/en-us/media/773afccb-4687-4b9f-8a89-8b32f640b27d.png")
    elif message['detail']['state'] == 'FAILED':
        state.activityText(activity_text)
        state.activityImage(
            "https://support.content.office.net/en-us/media/c9ed80c9-a24c-40b0-ba59-a6af25dc56fb.png")

    else:
        state.activityImage(
            "https://support.content.office.net/en-us/media/47588200-0bf0-46e9-977e-e668978f459c.png")

        state.text(message['detail']['state'])
    connection_card.addSection(state)


def lambda_handler(event, context):
    _help = ""
    print(event)
    #
    # Get event source
    #

    region = os.environ['AWS_REGION']
    message = event

    webhook_secret_url = get_secret()
    # message = json.loads(message)

    print(message)
    if message['source'] == "aws.codepipeline":
        team_message = pymsteams.connectorcard(webhook_secret_url)

        # create the section action
        state = pymsteams.cardsection()
        pipeline = message['detail']['pipeline']
        # Section Title
        state.title("State")

        if message["detail-type"] == "CodePipeline Action Execution State Change":

            team_message.title(
                f"Action Execution State Change - {message['detail-type']} in {pipeline} Pipeline")
            team_message.color("7b9683")
            stgs = json.loads(os.environ['approval_stages'])
            if os.environ['enable_chatops'] == "true" and message['detail']['action'] == stgs[0]["action_name"]:
                _help = f"\n \n Run @aws codepipeline get-pipeline-state --name {pipeline} --region {region}"
                status = get_pipeline_status(pipeline_name=pipeline)

                token = get_token(status=status, stage_name=stgs[0]["stage_name"], action_name=stgs[0]["action_name"])
                print(token)
                if token is not None:
                    _help += f"\n \n \n Run @aws codepipeline put-approval-result --pipeline-name {pipeline} " \
                             f"--stage-name {stgs[0]['stage_name']} --action-name {stgs[0]['action_name']} --token {token} " \
                             '--result status="Approved",summary="The new infra looks good. Ready to release to customers."'
            # Add text to the message.
            team_message.text(
                f"Action Execution State Change in pipeline {message['detail']['pipeline']} in account {message['account']} in region {message['region']} \n "

            )

            # create the section stage

            stage = pymsteams.cardsection()
            # create the section action
            action = pymsteams.cardsection()
            # Section Title
            action.title("Action")
            action.text(message['detail']['action'])

            team_message.summary("Approval deployment")
            team_message.addSection(stage)

            set_state(message=message, state=state, connection_card=team_message,
                      activity_text=f'Action Execution State Change! -Review if you need take action \n  {_help}')
            team_message.addSection(action)

            if 'execution-result' in message['detail']:
                # create the section result
                result = pymsteams.cardsection()
                # Section Title
                result.title("Result")
                summary = message['detail']['execution-result'].get('external-execution-summary', '')
                result_summ = message['detail']['execution-result'].get('external-execution-state', '')
                result_url = message['detail']['execution-result'].get('external-execution-url', '')
                result.text(f"{summary} - {result_summ}")
                if result_url != '':
                    team_message.addLinkButton("Go to the console",
                                               result_url)

                team_message.addSection(result)

        elif message["detail-type"] == "CodePipeline Pipeline Execution State Change":
            print("State change ... \n")
            team_message.title(
                f"State Change in {message['detail']['pipeline']} Pipeline")
            team_message.color("7b9683")
            # Add text to the message.
            team_message.text(
                f"Stage Change in pipeline {message['detail']['pipeline']} in account {message['account']} in region {message['region']} \n "

            )

            set_state(message=message, state=state, connection_card=team_message, activity_text='')

        elif message["detail-type"] == "CodePipeline Stage Execution State Change":

            print("Stage change ... \n")
            team_message.title(
                f"Stage Change in {message['detail']['pipeline']} Pipeline")
            team_message.color("7b9683")

            # Add text to the message.
            team_message.text(
                f"Stage Change in pipeline {message['detail']['pipeline']} in account {message['account']} in region {message['region']} \n "

            )
            pipeline = message['detail']['pipeline']
            # create the section stage

            stage = pymsteams.cardsection()
            # create the section action
            # Section Title
            stage.title(f"Stage {message['detail']['stage']}")
            set_state(message=message, state=state, connection_card=team_message,
                      activity_text="")

            team_message.summary("Stage Change")
            team_message.addSection(stage)

            team_message.addLinkButton("Go to the console",
                                       f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region={region}")

        team_message.send()

    if event['source'] == 'aws.codecommit':
        branch = event['detail']['referenceName']  # ['eventSource'][['ref']
        print(branch)
