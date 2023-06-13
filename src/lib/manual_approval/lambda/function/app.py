import json
import os

import pymsteams
from get_secret import get_secret
import json
from datetime import datetime


def lambda_handler(event, context):
    print(event)

    region = os.environ['AWS_REGION']
    message = event['Records'][0]['Sns']['Message']

    webhook_secret_url = get_secret()
    message = json.loads(message)

    print(message)
    if message['source'] == "aws.codepipeline":
        team_message = pymsteams.connectorcard(webhook_secret_url)

        if message["detailType"] == "CodePipeline Action Execution State Change":

            team_message.title(
                f"Manual Approval Update - {message['detailType']} in {message['detail']['pipeline']} Pipeline")
            team_message.color("7b9683")

            # Add text to the message.
            team_message.text(
                f"Change for manual Approval in pipeline {message['detail']['pipeline']} in account {message['account']} in region {message['region']} \n "

                )
            pipeline = message['detail']['pipeline']
            # create the section stage

            stage = pymsteams.cardsection()
            # create the section action
            action = pymsteams.cardsection()
            # Section Title
            action.title("Action")
            action.text(message['detail']['action'])

            # create the section action
            state = pymsteams.cardsection()
            # Section Title
            state.title("State")
            if message['detail']['state'] == 'STARTED':
                state.text(message['detail']['state'])
                state.activityText('Manual Action is required!')
                state.activityImage(
                    "https://support.content.office.net/en-us/media/6b8c0bff-7ddc-4bff-9101-8360f8c8a727.png")
            elif message['detail']['state'] == 'FAILED':
                state.activityText('Manual approval failed')
                state.activityImage(
                    "https://support.content.office.net/en-us/media/c9ed80c9-a24c-40b0-ba59-a6af25dc56fb.png")

            else:
                state.activityImage(
                    "https://support.content.office.net/en-us/media/773afccb-4687-4b9f-8a89-8b32f640b27d.png")

                state.text(message['detail']['state'])

            team_message.addLinkButton("Go to the console",
                                       f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region={region}")
            date = datetime.today().strftime("%Y/%m/%d")
            team_message.addLinkButton("Download Reports",
                                       f"https://s3.console.aws.amazon.com/s3/buckets/sophos-products-security-reports?region={region}&prefix=AccessAnalyzer/{date}/&showversions=false")

            team_message.summary("Approval deployment")
            team_message.addSection(stage)
            team_message.addSection(action)

            if 'execution-result' in message['detail']:
                # create the section result
                result = pymsteams.cardsection()
                # Section Title
                result.title("Result")
                result.text(message['detail']['execution-result']['external-execution-summary'])
                team_message.addSection(result)

            team_message.addSection(state)
            team_message.send()

        elif message["detailType"] == "CodePipeline Stage Execution State Change":
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
            action = pymsteams.cardsection()
            # Section Title
            stage.title(f"Stage {message['detail']['stage']}")

            if message['detail']['state'] == 'FAILED':
                print("State Failed")
                stage.text(message['detail']['state'])
                stage.activityImage(
                    "https://support.content.office.net/en-us/media/c9ed80c9-a24c-40b0-ba59-a6af25dc56fb.png")

            elif message['detail']['state'] == 'SUCCEEDED':
                print("State Succeeded")
                stage.text(message['detail']['state'])
                stage.activityImage(
                    "https://support.content.office.net/en-us/media/773afccb-4687-4b9f-8a89-8b32f640b27d.png")

            team_message.addLinkButton("Go to the console",
                                       f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region={region}")

            team_message.summary("State Change")
            team_message.addSection(stage)
            team_message.send()
